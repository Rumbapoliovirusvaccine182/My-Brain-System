import os
import json
import sys
import re
from pathlib import Path
import PyPDF2
import base64

# Import centralized config
from config import INBOX_DIR, AGENT_DIR

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def is_block_start(line):
    s = line.strip()
    # Headers
    if s.startswith('#'): return True
    # Ordered list markers "1." etc
    if re.match(r'^\d+\.?$', s) or re.match(r'^\d+\.\s', s): return True
    # Emojis used as bullets
    if s.startswith(('❌', '⚠', '👉', '✅')): return True
    # Source line
    if s.startswith('Source:'): return True
    return False

def is_cjk(char):
    if not char: return False
    code = ord(char)
    return (0x4E00 <= code <= 0x9FFF or  # CJK Unified Ideographs
            0x3040 <= code <= 0x309F or  # Hiragana
            0x30A0 <= code <= 0x30FF or  # Katakana
            0xFF00 <= code <= 0xFFEF)    # Full-width characters

def clean_extracted_text(text):
    """
    Polite heuristic to fix corrupted PDF text where each character is on a new line.
    Also handles merging CJK characters without spaces while formatting English correctly.
    """
    lines = text.splitlines()
    result_body = []
    space_lines = 0
    first_line = True
    last_line_content = ""

    for line in lines:
        s = line.strip()
        
        if not s:
            space_lines += 1
            continue

        # Determine separator
        sep = ""
        if first_line:
            sep = ""
        elif space_lines >= 2:
            # If there were multiple blank lines, treat as paragraph break
            sep = "\n\n"
        elif space_lines == 1:
             if is_block_start(s):
                sep = "\n\n"
             else:
                # Merge logic - treating single blank line as just wrapping in messy PDFs
                if last_line_content and is_cjk(last_line_content[-1]) and is_cjk(s[0]):
                    sep = ""
                else:
                    sep = " "
        else: # space_lines == 0 (adjacent lines)
            if is_block_start(s):
                sep = "\n\n" # Force break for new blocks
            else:
                # Merge logic
                # If CJK -> merge without space
                # If English/Latin -> merge with space
                if last_line_content and is_cjk(last_line_content[-1]) and is_cjk(s[0]):
                    sep = ""
                else:
                    sep = " "

        # Special handling for headers: ensure strictly \n\n before
        if s.startswith('#') and not first_line and not sep.startswith('\n\n'):
             sep = "\n\n"

        result_body.append(sep + s)
        
        last_line_content = s
        space_lines = 0
        first_line = False

    return "".join(result_body)

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # Remove surrogate characters that break JSON serialization
            text = text.encode('utf-8', errors='replace').decode('utf-8')
            # Post-process the extracted text to fix formatting issues
            cleaned_text = clean_extracted_text(text.strip())
            return cleaned_text
            
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def encode_image_base64(image_path):
    """Encode image to base64"""
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        return f"Error encoding image: {str(e)}"

def process_inbox():
    """Process all files in 00_Inbox"""
    results = []
    
    # Check if inbox exists
    if not INBOX_DIR.exists():
        print(f"Inbox directory not found: {INBOX_DIR}")
        return []

    for file_path in sorted(INBOX_DIR.iterdir()):
        if file_path.is_file():
            file_info = {
                "filename": file_path.name,
                "extension": file_path.suffix.lower(),
                "size": file_path.stat().st_size
            }
            
            if file_path.suffix.lower() == '.pdf':
                file_info["content"] = extract_pdf_text(file_path)
                file_info["type"] = "pdf"
            elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                # For images, we'll just note them - actual analysis will be done by AI
                file_info["type"] = "image"
                file_info["content"] = "[Image file - requires AI analysis]"
            
            results.append(file_info)
    
    return results

if __name__ == "__main__":
    results = process_inbox()
    # Write to file with explicit UTF-8 encoding
    output_path = AGENT_DIR / "inbox_content.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Processed {len(results)} files. Output saved to {output_path}")
