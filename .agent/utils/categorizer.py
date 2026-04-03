"""
Categorization utilities for My Brain knowledge management system
"""
from typing import Dict, List, Optional, Tuple
from . import taxonomy_loader


def score_category(content: str, keywords: List[str]) -> int:
    """
    Score how well content matches a category based on keyword frequency
    
    Args:
        content: Text content to analyze (title + tags + content)
        keywords: List of keywords for the category
        
    Returns:
        Score (number of keyword matches)
    """
    content_lower = content.lower()
    score = sum(1 for keyword in keywords if keyword.lower() in content_lower)
    return score


def determine_category(note_content: str, note_title: str = "", note_tags: List[str] = None, 
                      taxonomy: Optional[Dict] = None) -> str:
    """
    Determine the best category for a note based on content analysis
    
    Args:
        note_content: Full note content
        note_title: Note title (optional, for better matching)
        note_tags: Note tags (optional, for better matching)
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        Category name
    """
    if taxonomy is None:
        taxonomy = taxonomy_loader.load_taxonomy()
    
    if note_tags is None:
        note_tags = []
    
    # Combine title, tags, and content for analysis
    analysis_text = f"{note_title} {' '.join(note_tags)} {note_content}"
    
    # Score each category
    scores = {}
    for cat_name, cat_info in taxonomy.items():
        if cat_name == 'General':
            continue  # Skip General, it's the fallback
        
        keywords = cat_info.get('keywords', [])
        scores[cat_name] = score_category(analysis_text, keywords)
    
    # Determine best category
    if not scores or max(scores.values()) == 0:
        return 'General'
    
    return max(scores, key=scores.get)


def find_subcategory(category: str, note_content: str, note_title: str = "", 
                    note_tags: List[str] = None, taxonomy: Optional[Dict] = None) -> Optional[str]:
    """
    Find the best subcategory within a category
    
    Args:
        category: Parent category name
        note_content: Full note content
        note_title: Note title (optional)
        note_tags: Note tags (optional)
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        Subcategory name or None if no good match
    """
    if taxonomy is None:
        taxonomy = taxonomy_loader.load_taxonomy()
    
    if note_tags is None:
        note_tags = []
    
    # Get subcategories for this category
    subcategories = taxonomy.get(category, {}).get('subcategories', {})
    
    if not subcategories:
        return None
    
    # Combine title, tags, and content for analysis
    analysis_text = f"{note_title} {' '.join(note_tags)} {note_content}"
    
    # Score each subcategory
    scores = {}
    for subcat_name, subcat_info in subcategories.items():
        keywords = subcat_info.get('keywords', [])
        scores[subcat_name] = score_category(analysis_text, keywords)
    
    # Return best subcategory if score > 0
    if not scores or max(scores.values()) == 0:
        return None
    
    return max(scores, key=scores.get)


def categorize_note(note_content: str, note_title: str = "", note_tags: List[str] = None,
                   taxonomy: Optional[Dict] = None) -> Tuple[str, Optional[str]]:
    """
    Fully categorize a note (category + subcategory)
    
    Args:
        note_content: Full note content
        note_title: Note title (optional)
        note_tags: Note tags (optional)
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        Tuple of (category, subcategory) where subcategory may be None
    """
    if taxonomy is None:
        taxonomy = taxonomy_loader.load_taxonomy()
    
    # Determine category
    category = determine_category(note_content, note_title, note_tags, taxonomy)
    
    # Determine subcategory
    subcategory = find_subcategory(category, note_content, note_title, note_tags, taxonomy)
    
    return category, subcategory


def get_category_scores(note_content: str, note_title: str = "", note_tags: List[str] = None,
                       taxonomy: Optional[Dict] = None) -> Dict[str, int]:
    """
    Get scores for all categories (useful for debugging/analysis)
    
    Args:
        note_content: Full note content
        note_title: Note title (optional)
        note_tags: Note tags (optional)
        taxonomy: Taxonomy dictionary (will load if not provided)
        
    Returns:
        Dictionary mapping category names to scores
    """
    if taxonomy is None:
        taxonomy = taxonomy_loader.load_taxonomy()
    
    if note_tags is None:
        note_tags = []
    
    # Combine title, tags, and content for analysis
    analysis_text = f"{note_title} {' '.join(note_tags)} {note_content}"
    
    # Score each category
    scores = {}
    for cat_name, cat_info in taxonomy.items():
        if cat_name == 'General':
            continue
        
        keywords = cat_info.get('keywords', [])
        scores[cat_name] = score_category(analysis_text, keywords)
    
    return scores
