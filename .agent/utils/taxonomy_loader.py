"""
Taxonomy loader for My Brain knowledge management system
Loads and parses taxonomy.md for category definitions
"""
import re
from pathlib import Path
from typing import Dict, List, Optional
from . import file_ops


def load_taxonomy(taxonomy_path: Optional[Path] = None) -> Dict[str, Dict]:
    """
    Load taxonomy from taxonomy.md file
    
    Args:
        taxonomy_path: Path to taxonomy.md (default: .agent/taxonomy.md)
        
    Returns:
        Dictionary of category definitions with keywords and subcategories
    """
    if taxonomy_path is None:
        import config
        taxonomy_path = config.AGENT_DIR / "taxonomy.md"
    
    if not taxonomy_path.exists():
        raise FileNotFoundError(f"Taxonomy file not found: {taxonomy_path}")
    
    content = file_ops.read_markdown(taxonomy_path)
    
    taxonomy = {}
    
    # Split by ## headers (category sections)
    category_sections = re.split(r'\n## ', content)
    
    for section in category_sections[1:]:  # Skip preamble
        lines = section.split('\n')
        category_name = lines[0].strip()
        
        # Skip non-category sections
        if category_name in ['Usage Guidelines', 'Categorization Rules', 'Threshold Guidelines', 
                              'Adding New Categories', 'Adding New Subcategories']:
            continue
        
        # Extract description
        description_match = re.search(r'\*\*Description\*\*:\s*(.+)', section)
        description = description_match.group(1).strip() if description_match else ""
        
        # Extract keywords
        keywords = []
        keywords_section = re.search(r'\*\*Keywords\*\*:\s*\n(.*?)(?:\n\*\*Keywords\*\*|\n###|\n---|$)', section, re.DOTALL)
        if keywords_section:
            keywords_text = keywords_section.group(1)
            # Extract all keywords from bullet points or comma-separated list
            for line in keywords_text.split('\n'):
                line = line.strip()
                if not line: continue
                if line.startswith('-'):
                    items = line[1:].split(',')
                else:
                    items = line.split(',')
                keywords.extend([k.strip() for k in items if k.strip()])
        
        # Extract subcategories (recursive)
        subcategories = {}
        
        # Find all subcategory headers (### and ####)
        # We process them in order and maintain a hierarchy stack
        header_pattern = re.compile(r'^(#{3,6})\s+(.+)$', re.MULTILINE)
        
        # Split section into chunks by header to process content
        # This is a bit complex, so we'll use a simpler approach: 
        # Scan for ### headers, then within those scan for ####
        
        subcat_matches = list(re.finditer(r'### (.+?)\n(.*?)(?=\n###|\n---|\Z)', section, re.DOTALL))
        
        for match in subcat_matches:
            subcat_full_name = match.group(1).strip()
            # Remove category prefix if it exists to prevent duplication
            if subcat_full_name.startswith(f"{category_name}/"):
                subcat_full_name = subcat_full_name[len(category_name)+1:]
            subcat_content = match.group(2)
            
            # Helper to extract metadata from content block
            def extract_meta(text):
                desc_m = re.search(r'\*\*Description\*\*:\s*(.+)', text)
                desc = desc_m.group(1).strip() if desc_m else ""
                
                kw_m = re.search(r'\*\*Keywords\*\*:\s*(.+)', text)
                kw = [k.strip() for k in kw_m.group(1).split(',')] if kw_m else []
                return desc, kw

            sc_desc, sc_kw = extract_meta(subcat_content)
            
            # Base subcategory (e.g., AI_Hardware)
            # If name implies hierarchy (AI_Hardware/NVIDIA), handle it
            parts = subcat_full_name.split('/')
            base_name = parts[0]
            
            if base_name not in subcategories:
                subcategories[base_name] = {
                    'description': sc_desc,
                    'keywords': sc_kw,
                    'subcategories': {}
                }
            else:
                 # Update if already exists (might have been created by a child)
                 if sc_desc: subcategories[base_name]['description'] = sc_desc
                 if sc_kw: subcategories[base_name]['keywords'].extend(sc_kw)
            
            # Handle nesting (AI_Hardware/NVIDIA_Ecosystem)
            current_level = subcategories[base_name]
            for part in parts[1:]:
                if part not in current_level['subcategories']:
                    current_level['subcategories'][part] = {
                        'description': sc_desc, # Inherit or overwrite? Usually leaf has specific desc
                        'keywords': sc_kw,
                        'subcategories': {}
                    }
                current_level = current_level['subcategories'][part]
            
            # If we are validly processing a deeper level here, update its specific metadata
            # The regex captured the specific block for this full name
            if len(parts) > 1:
                current_level['description'] = sc_desc
                current_level['keywords'] = sc_kw
            
            # Should look for #### inside this block if not using / notation?
            # Current taxonomy uses #### AI_Hardware/NVIDIA_Ecosystem
            # So the above split logic handles the flattened Markdown header style perfectly.

        taxonomy[category_name] = {
            'description': description,
            'keywords': keywords,
            'subcategories': subcategories
        }
    
    return taxonomy


def get_category_keywords(category: str, taxonomy: Optional[Dict] = None) -> List[str]:
    """
    Get keywords for a specific category
    
    Args:
        category: Category name
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        List of keywords for the category
    """
    if taxonomy is None:
        taxonomy = load_taxonomy()
    
    return taxonomy.get(category, {}).get('keywords', [])


def get_subcategories(category: str, taxonomy: Optional[Dict] = None) -> Dict[str, Dict]:
    """
    Get subcategories for a specific category
    
    Args:
        category: Category name
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        Dictionary of subcategory definitions
    """
    if taxonomy is None:
        taxonomy = load_taxonomy()
    
    return taxonomy.get(category, {}).get('subcategories', {})


def get_subcategory_keywords(category: str, subcategory: str, taxonomy: Optional[Dict] = None) -> List[str]:
    """
    Get keywords for a specific subcategory
    
    Args:
        category: Category name
        subcategory: Subcategory name
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        List of keywords for the subcategory
    """
    if taxonomy is None:
        taxonomy = load_taxonomy()
    
    subcats = taxonomy.get(category, {}).get('subcategories', {})
    return subcats.get(subcategory, {}).get('keywords', [])


def get_all_categories(taxonomy: Optional[Dict] = None) -> List[str]:
    """
    Get list of all category names
    
    Args:
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        List of category names
    """
    if taxonomy is None:
        taxonomy = load_taxonomy()
    
    return list(taxonomy.keys())
