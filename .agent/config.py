"""
Centralized configuration for My Brain knowledge management system
"""
from pathlib import Path

# ============================================================================
# Directory Paths
# ============================================================================

# Root directory (parent of .agent)
BRAIN_ROOT = Path(__file__).parent.parent

# Main directories
INBOX_DIR = BRAIN_ROOT / "00_Inbox"
GARDEN_DIR = BRAIN_ROOT / "10_Garden"
PROJECTS_DIR = BRAIN_ROOT / "20_Projects"
ARCHIVES_DIR = BRAIN_ROOT / "99_Archives"
ASSETS_DIR = ARCHIVES_DIR / "Assets"
AGENT_DIR = BRAIN_ROOT / ".agent"

# Project directories (optional — enable if using project management features)
# TEMPLATES_DIR = PROJECTS_DIR / "_Templates"
# CONSULTING_DIR = PROJECTS_DIR / "Consulting"
# INVESTMENTS_DIR = PROJECTS_DIR / "Investments"
# ARCHIVED_PROJECTS_DIR = ARCHIVES_DIR / "Projects"

# Lab directories
LAB_DIR = BRAIN_ROOT / "30_Lab"
LAB_THESES_DIR = LAB_DIR / "Theses"
LAB_ESSAYS_DIR = LAB_DIR / "Essays"
LAB_SCRATCH_DIR = LAB_DIR / "Scratch"
ARCHIVED_LAB_DIR = ARCHIVES_DIR / "Lab"

# Gap reports
GAPS_DIR = AGENT_DIR / "gaps"

# ============================================================================
# Category Definitions
# ============================================================================

CATEGORIES = {
    'AI_Hardware': {
        'description': 'AI hardware: compute silicon, memory, networking/optics, packaging/mfg, infra/power, testing',
        'subcategories': ['Compute', 'Memory_Storage', 'Networking_Optics', 'Packaging_Mfg', 'Infra_Power', 'Testing']
    },
    'AI_Software': {
        'description': 'AI applications, software trends, and consumer AI products',
        'subcategories': ['Applications', 'Software_Trends', 'Products']
    },
    'Industry_Verticals': {
        'description': 'Non-AI industry analysis: automotive, energy, space, robotics, materials',
        'subcategories': ['Automotive_Tech', 'Clean_Energy', 'Space_Telecom', 'Robotics_Automation', 'Commodities_Materials']
    },
    'Investment_Thinking': {
        'description': 'Investment psychology, frameworks, trading systems, valuation',
        'subcategories': ['Investor_Mindset', 'Market_Behavior', 'Frameworks', 'Trading_Systems', 'Valuation_Models']
    },
    'Macro_Markets': {
        'description': 'Geopolitical analysis, macro trends, portfolio-level decisions',
        'subcategories': ['Geopolitics', 'Portfolio_Reviews']
    },
    'Journal': {
        'description': 'Personal reflections, journals, essays, career development',
        'subcategories': []
    },
    'Parenting': {
        'description': 'Education, parenting, and family activities',
        'subcategories': []
    },
}

# ============================================================================
# Thresholds
# ============================================================================

CATEGORY_SIZE_THRESHOLDS = {
    'small': 5,       # < 5 notes: Consider merging
    'ideal_min': 5,   # 5-20 notes: Ideal leaf size
    'ideal_max': 20,  # Target range upper bound
    'large': 20,      # > 20 notes: Suggest subdivision
    'very_large': 30  # > 30 notes: Strongly recommend subdivision
}

# ============================================================================
# File Patterns
# ============================================================================

MARKDOWN_EXTENSIONS = ['.md', '.markdown']
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
PDF_EXTENSIONS = ['.pdf']
OFFICE_EXTENSIONS = ['.pptx', '.docx', '.xlsx', '.msg', '.eml']
SUPPORTED_EXTENSIONS = MARKDOWN_EXTENSIONS + IMAGE_EXTENSIONS + PDF_EXTENSIONS + OFFICE_EXTENSIONS

# Files to exclude from processing
# Note: Topic indices now use pattern [FolderName]_主題索引.md
EXCLUDE_FILES = ['README.md', 'Dashboard.md']

def is_topic_index(filename: str) -> bool:
    """Check if a file is a topic index file"""
    return filename.endswith('_主題索引.md')

# ============================================================================
# YAML Frontmatter Defaults
# ============================================================================

DEFAULT_FRONTMATTER = {
    'created': None,  # Will be set to current date
    'updated': None,  # Will be set to current date
    'tags': [],
    'source_type': None,
    'source_asset': None
}

# ============================================================================
# Validation
# ============================================================================

def validate_paths():
    """Validate that all required directories exist"""
    required_dirs = [BRAIN_ROOT, INBOX_DIR, GARDEN_DIR, PROJECTS_DIR, ARCHIVES_DIR, AGENT_DIR]
    missing = [d for d in required_dirs if not d.exists()]
    
    if missing:
        raise FileNotFoundError(
            f"Missing required directories: {[str(d) for d in missing]}\n"
            f"Expected BRAIN_ROOT at: {BRAIN_ROOT}"
        )

# Validate on import
try:
    validate_paths()
except FileNotFoundError as e:
    import warnings
    warnings.warn(f"Configuration validation failed: {e}")

# ============================================================================
# Utility Functions
# ============================================================================

def get_category_dir(category: str) -> Path:
    """Get the directory path for a category"""
    return GARDEN_DIR / category

def get_subcategory_dir(category: str, subcategory: str) -> Path:
    """Get the directory path for a subcategory"""
    return GARDEN_DIR / category / subcategory

def is_valid_category(category: str) -> bool:
    """Check if a category name is valid"""
    return category in CATEGORIES

def get_subcategories(category: str) -> list:
    """Get list of subcategories for a category"""
    return CATEGORIES.get(category, {}).get('subcategories', [])
