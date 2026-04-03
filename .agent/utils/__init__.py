"""
Shared utilities for My Brain knowledge management system
"""

from .file_ops import (
    read_markdown,
    write_markdown,
    read_json,
    write_json,
    safe_move,
    ensure_dir,
    list_markdown_files
)

from .markdown_parser import (
    extract_yaml_frontmatter,
    extract_wikilinks,
    extract_tags,
    parse_note,
    create_yaml_frontmatter,
    NoteMetadata
)

from .taxonomy_loader import (
    load_taxonomy,
    get_category_keywords,
    get_subcategories,
    get_subcategory_keywords,
    get_all_categories
)

from .categorizer import (
    score_category,
    determine_category,
    find_subcategory,
    categorize_note,
    get_category_scores
)

from .wikilink_manager import (
    scan_all_notes,
    check_wikilinks,
    update_wikilinks_after_move,
    remove_dead_links,
    get_link_stats
)

from .template_engine import (
    populate_template,
    create_from_template,
    list_templates
)

from .project_scanner import (
    get_project_brief,
    get_open_action_items,
    get_recent_decisions,
    get_ad_hoc_items,
    get_project_status,
    list_active_projects
)

__all__ = [
    # File operations
    'read_markdown',
    'write_markdown',
    'read_json',
    'write_json',
    'safe_move',
    'ensure_dir',
    'list_markdown_files',
    
    # Markdown parsing
    'extract_yaml_frontmatter',
    'extract_wikilinks',
    'extract_tags',
    'parse_note',
    'create_yaml_frontmatter',
    'NoteMetadata',
    
    # Taxonomy
    'load_taxonomy',
    'get_category_keywords',
    'get_subcategories',
    'get_subcategory_keywords',
    'get_all_categories',
    
    # Categorization
    'score_category',
    'determine_category',
    'find_subcategory',
    'categorize_note',
    'get_category_scores',

    # WikiLink management
    'scan_all_notes',
    'check_wikilinks',
    'update_wikilinks_after_move',
    'remove_dead_links',
    'get_link_stats',

    # Template engine
    'populate_template',
    'create_from_template',
    'list_templates',

    # Project scanner
    'get_project_brief',
    'get_open_action_items',
    'get_recent_decisions',
    'get_ad_hoc_items',
    'get_project_status',
    'list_active_projects',
]
