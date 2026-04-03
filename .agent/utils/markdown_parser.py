"""
Markdown parsing utilities for My Brain knowledge management system
"""
import re
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class NoteMetadata:
    """Metadata extracted from a markdown note"""
    filename: str
    title: str
    tags: List[str]
    created: Optional[str]
    updated: Optional[str]
    source_type: Optional[str]
    source_asset: Optional[str]
    word_count: int
    wikilinks: List[str]
    modified_time: float


def extract_yaml_frontmatter(content: str) -> Dict[str, any]:
    """
    Extract YAML frontmatter from markdown content
    
    Args:
        content: Markdown file content
        
    Returns:
        Dictionary of YAML data
    """
    yaml_data = {}
    
    # Match YAML frontmatter between --- delimiters
    yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    
    if not yaml_match:
        return yaml_data
    
    yaml_text = yaml_match.group(1)
    
    # Parse title
    title_match = re.search(r'title:\s*(.+)', yaml_text)
    if title_match:
        yaml_data['title'] = title_match.group(1).strip()
    
    # Parse tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', yaml_text)
    if tags_match:
        tags_str = tags_match.group(1)
        yaml_data['tags'] = [t.strip() for t in tags_str.split(',') if t.strip()]
    else:
        yaml_data['tags'] = []
    
    # Parse created date
    created_match = re.search(r'created:\s*(.+)', yaml_text)
    if created_match:
        yaml_data['created'] = created_match.group(1).strip()
    
    # Parse updated date
    updated_match = re.search(r'updated:\s*(.+)', yaml_text)
    if updated_match:
        yaml_data['updated'] = updated_match.group(1).strip()
    
    # Parse source_type
    source_type_match = re.search(r'source_type:\s*(.+)', yaml_text)
    if source_type_match:
        yaml_data['source_type'] = source_type_match.group(1).strip()
    
    # Parse source_asset
    source_asset_match = re.search(r'source_asset:\s*(.+)', yaml_text)
    if source_asset_match:
        yaml_data['source_asset'] = source_asset_match.group(1).strip()
    
    return yaml_data


def extract_wikilinks(content: str) -> List[str]:
    """
    Extract all WikiLinks from markdown content
    
    Args:
        content: Markdown file content
        
    Returns:
        List of WikiLink targets (without brackets)
    """
    # Pattern: [[Link Text]] or [[Link Text|Display Text]]
    pattern = r'\[\[([^\]]+?)\]\]'
    matches = re.findall(pattern, content)
    
    links = []
    for match in matches:
        # Handle [[Link|Display]] format
        if '|' in match:
            link = match.split('|')[0].strip()
        else:
            link = match.strip()
        links.append(link)
    
    return links


def extract_tags(content: str) -> List[str]:
    """
    Extract tags from YAML frontmatter
    
    Args:
        content: Markdown file content
        
    Returns:
        List of tags
    """
    yaml_data = extract_yaml_frontmatter(content)
    return yaml_data.get('tags', [])


def parse_note(path: Path) -> NoteMetadata:
    """
    Parse a markdown note and extract all metadata
    
    Args:
        path: Path to markdown file
        
    Returns:
        NoteMetadata object with extracted information
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    yaml_data = extract_yaml_frontmatter(content)
    
    # Extract WikiLinks
    wikilinks = extract_wikilinks(content)
    
    # Get file stats
    stat = path.stat()
    
    return NoteMetadata(
        filename=path.name,
        title=yaml_data.get('title', path.stem),
        tags=yaml_data.get('tags', []),
        created=yaml_data.get('created'),
        updated=yaml_data.get('updated'),
        source_type=yaml_data.get('source_type'),
        source_asset=yaml_data.get('source_asset'),
        word_count=len(content),
        wikilinks=wikilinks,
        modified_time=stat.st_mtime
    )


def create_yaml_frontmatter(metadata: Dict[str, any]) -> str:
    """
    Create YAML frontmatter from metadata dictionary
    
    Args:
        metadata: Dictionary of metadata fields
        
    Returns:
        YAML frontmatter string (including --- delimiters)
    """
    lines = ['---']
    
    # Add title
    if 'title' in metadata:
        lines.append(f"title: {metadata['title']}")
    
    # Add dates
    if 'created' in metadata:
        lines.append(f"created: {metadata['created']}")
    if 'updated' in metadata:
        lines.append(f"updated: {metadata['updated']}")
    
    # Add tags
    if 'tags' in metadata and metadata['tags']:
        tags_str = ', '.join(metadata['tags'])
        lines.append(f"tags: [{tags_str}]")
    
    # Add source info
    if 'source_type' in metadata:
        lines.append(f"source_type: {metadata['source_type']}")
    if 'source_asset' in metadata:
        lines.append(f"source_asset: {metadata['source_asset']}")
    
    lines.append('---')
    return '\n'.join(lines)


def remove_yaml_frontmatter(content: str) -> str:
    """
    Remove YAML frontmatter from markdown content
    
    Args:
        content: Markdown file content
        
    Returns:
        Content without frontmatter
    """
    # Remove YAML frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL | re.MULTILINE)
    return content.strip()


def extract_summary(content: str) -> Optional[str]:
    """
    Extract summary/摘要 section from markdown content
    
    Args:
        content: Markdown file content
        
    Returns:
        Summary text (first paragraph under ## 摘要 or ## Summary), or None if not found
    """
    # Remove frontmatter first
    content_without_yaml = remove_yaml_frontmatter(content)
    
    # Try to find 摘要 (Summary) section
    summary_patterns = [
        r'##\s*摘要\s*\(Summary\)\s*\n+(.*?)(?=\n##|\Z)',  # ## 摘要 (Summary)
        r'##\s*Summary\s*\n+(.*?)(?=\n##|\Z)',             # ## Summary
        r'##\s*摘要\s*\n+(.*?)(?=\n##|\Z)',                # ## 摘要
    ]
    
    for pattern in summary_patterns:
        match = re.search(pattern, content_without_yaml, re.DOTALL)
        if match:
            summary = match.group(1).strip()
            # Get first paragraph only (up to double newline or end)
            first_para = summary.split('\n\n')[0].strip()
            # Remove any markdown formatting for cleaner display
            first_para = re.sub(r'\*\*(.+?)\*\*', r'\1', first_para)  # Remove bold
            first_para = re.sub(r'\*(.+?)\*', r'\1', first_para)      # Remove italic
            first_para = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', first_para)  # Remove links
            return first_para
    
    return None


def extract_key_insights(content: str, max_insights: int = 3) -> List[str]:
    """
    Extract key insights from 關鍵洞察 section
    
    Args:
        content: Markdown file content
        max_insights: Maximum number of insights to extract
        
    Returns:
        List of key insight strings
    """
    # Remove frontmatter first
    content_without_yaml = remove_yaml_frontmatter(content)
    
    # Try to find 關鍵洞察 (Key Insights) section
    insight_patterns = [
        r'##\s*關鍵洞察\s*\(Key Insights\)\s*\n+(.*?)(?=\n##|\Z)',
        r'##\s*Key Insights\s*\n+(.*?)(?=\n##|\Z)',
        r'##\s*關鍵洞察\s*\n+(.*?)(?=\n##|\Z)',
    ]
    
    for pattern in insight_patterns:
        match = re.search(pattern, content_without_yaml, re.DOTALL)
        if match:
            insights_text = match.group(1).strip()
            # Extract numbered list items (1. **Title**: content)
            insight_items = re.findall(r'\d+\.\s*\*\*(.+?)\*\*:?\s*(.+?)(?=\n\d+\.|\Z)', insights_text, re.DOTALL)
            
            insights = []
            for title, content in insight_items[:max_insights]:
                # Clean up the content
                content_clean = content.strip().split('\n')[0]  # First line only
                insights.append(f"{title.strip()}: {content_clean[:100]}...")
            
            return insights
    
    return []

