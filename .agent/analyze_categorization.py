"""
Analyze Garden notes and propose categorization
Refactored to support Global Re-homing and Recursive Subdivision
"""
import sys
from pathlib import Path
from collections import defaultdict, Counter

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import shared utilities
from utils import (
    parse_note,
    write_json,
    load_taxonomy,
    list_markdown_files
)
import config

def score_category_recursive(analysis_text, category_def, current_path=""):
    """
    Recursively find the best matching category/subcategory path
    Returns: (best_path, best_score, best_depth)
    """
    best_path = current_path
    best_score = 0
    
    # helper for keyword matching
    def calculate_score(text, keywords):
        return sum(1 for k in keywords if k.lower() in text.lower())

    
    
    # Calculate score for current level
    current_keywords = category_def.get('keywords', [])
    match_count = calculate_score(analysis_text, current_keywords)
    
    # Squared depth weighting to heavily favor specific subcategories
    if match_count > 0:
        depth = len(current_path.split('/'))
        current_score = match_count * (depth ** 2)
    else:
        current_score = 0
    
    if current_score > best_score:
        best_score = current_score
        
    # Check subcategories
    subcats = category_def.get('subcategories', {})
    for sub_name, sub_def in subcats.items():
        sub_path = f"{current_path}/{sub_name}" if current_path else sub_name
        
        # Recursive call
        child_path, child_score, _ = score_category_recursive(analysis_text, sub_def, sub_path)
        
        if child_score > best_score:
            best_score = child_score
            best_path = child_path
            
    return best_path, best_score, 0

def find_best_fit(note_metadata, taxonomy):
    """
    Find the absolute best category for a note across the ENTIRE taxonomy.
    Global Re-homing Logic.
    """
    analysis_text = f"{note_metadata.title} {' '.join(note_metadata.tags)}".lower()
    
    best_global_score = 0
    best_global_path = "General"
    
    for cat_name, cat_def in taxonomy.items():
        # General is fallback
        if cat_name == 'General': continue
        
        path, score, _ = score_category_recursive(analysis_text, cat_def, cat_name)
        
        if score > best_global_score:
            best_global_score = score
            best_global_path = path
            
    # If no match, and current path is valid, keep it? 
    # Or return General if score 0?
    if best_global_score == 0:
        return "General"
        
    return best_global_path

def analyze_categorization():
    """Analyze all notes and propose categorization"""
    
    # Load taxonomy
    taxonomy = load_taxonomy()
    
    markdown_files = list_markdown_files(config.GARDEN_DIR, recursive=True, exclude=config.EXCLUDE_FILES)
    
    notes_analysis = []
    
    # 1. Global Re-homing Analysis
    print("=" * 80)
    print("PHASE 1: GLOBAL RE-HOMING ANALYSIS")
    print("=" * 80)
    
    category_counts = Counter()
    
    for md_file in markdown_files:
        try:
            note_metadata = parse_note(md_file)
            current_rel_path = md_file.relative_to(config.GARDEN_DIR).parent
            
            # Normalize current path (Windows sep -> POSIX)
            current_path_str = str(current_rel_path).replace('\\', '/')
            if current_path_str == '.': current_path_str = "Root"
            
            # Find best fit
            best_fit_path = find_best_fit(note_metadata, taxonomy)
            
            # Check if move needed
            # Simple check: is the start of best_fit_path matching current category?
            # Or strict match? 
            # If current is "AI_Tech/AI_Hardware" and best is "AI_Tech/AI_Hardware/NVIDIA", that is a Refinement (Split), not necessarily a Move, but we can treat as Move.
            
            # Let's count it for the "Subdivision" phase
            category_counts[best_fit_path] += 1
            
            notes_analysis.append({
                'filename': note_metadata.filename,
                'current_path': current_path_str,
                'proposed_path': best_fit_path,
                'title': note_metadata.title
            })
            
            if current_path_str != best_fit_path and best_fit_path != "General":
                # Don't spam moves to General
                pass 
                
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    # Print Move Suggestions
    moves = [n for n in notes_analysis if n['current_path'] != n['proposed_path'] and n['proposed_path'] != "General"]
    if moves:
        print(f"\n🔍 Found {len(moves)} notes that should be moved:")
        for m in moves[:10]: # Limit output
            print(f"  - {m['title']}")
            print(f"    Current: {m['current_path']} -> Proposed: {m['proposed_path']}")
        if len(moves) > 10: print(f"    ... and {len(moves)-10} more")
    else:
        print("\n✅ All notes appear to be in their best matching categories.")

    # 2. Recursive Subdivision Analysis
    print("\n" + "=" * 80)
    print("PHASE 2: RECURSIVE SUBDIVISION ANALYSIS")
    print("=" * 80)
    
    # We analyze based on the Proposed Path (assuming moves happen)
    # Construct a tree of counts
    
    # Analyze which 'Leaf' paths are valid from Taxonomy vs. which are overcrowded
    # Actually, we should check: if a folder has > Threshold, do we have sub-definitions?
    
    # Group notes by their 'Base' category for subdivision checks
    # If best_fit_path is 'AI_Tech/AI_Hardware', we count it there.
    
    final_counts = Counter()
    for n in notes_analysis:
        final_counts[n['proposed_path']] += 1
        
    threshold = config.CATEGORY_SIZE_THRESHOLDS['large'] # 30
    
    for path, count in final_counts.items():
        if count > threshold:
            print(f"\n⚠️ {path} has {count} notes (Threshold: {threshold})")
            
            # Check if this path has children in taxonomy
            # Walk the taxonomy to find definition
            parts = path.split('/')
            current_def = taxonomy.get(parts[0])
            valid_path = True
            
            if current_def:
                for part in parts[1:]:
                    if 'subcategories' in current_def and part in current_def['subcategories']:
                        current_def = current_def['subcategories'][part]
                    else:
                        valid_path = False
                        break
            
            if valid_path and current_def and current_def.get('subcategories'):
                print(f"  💡 Suggestion: Subdivide into:")
                subcats = current_def['subcategories']
                for sub_k in subcats.keys():
                    print(f"     - {path}/{sub_k}")
            else:
                print(f"  ℹ️  No deeper specific subcategories defined in Taxonomy.")
                print(f"      Action: Add new definitions to taxonomy.md to enable splitting.")

    # Save detailed analysis
    output_path = config.AGENT_DIR / "garden_categorization.json"
    
    # Transform for compatibility with deploy scripts if needed, or new format
    # The legacy deploy script expects 'category', 'subcategory'. 
    # We should normalize 'proposed_path' -> category/subcategory
    
    export_data = []
    for n in notes_analysis:
        parts = n['proposed_path'].split('/')
        cat = parts[0]
        sub = '/'.join(parts[1:]) if len(parts) > 1 else None
        
        export_data.append({
            'filename': n['filename'],
            'title': n['title'],
            'category': cat,
            'subcategory': sub,
            'relative_path': n['current_path'] + "/" + n['filename'] if n['current_path'] != "Root" else n['filename']
        })
        
    write_json(output_path, export_data)
    print(f"\n✓ Detailed analysis saved to {output_path.relative_to(config.BRAIN_ROOT)}")

if __name__ == "__main__":
    analyze_categorization()
