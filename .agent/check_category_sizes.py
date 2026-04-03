"""
Check category sizes and recommend subdivisions.
"""
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config

SMALL = config.CATEGORY_SIZE_THRESHOLDS['small']
MEDIUM = config.CATEGORY_SIZE_THRESHOLDS['medium']
LARGE = config.CATEGORY_SIZE_THRESHOLDS['large']

garden_dir = config.GARDEN_DIR

print("=" * 80)
print("CATEGORY SIZE ANALYSIS")
print("=" * 80)

categories = []


def check_dir(dir_path, depth=0):
    """Recursively check directory sizes."""
    indent = "  " * depth
    subdirs = [d for d in dir_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    md_files = [f for f in dir_path.glob("*.md") if not config.is_topic_index(f.name) and f.name not in config.EXCLUDE_FILES]

    if subdirs:
        print(f"\n{indent}📁 {dir_path.name} ({len(subdirs)} subcategories, {len(md_files)} direct notes)")
        for subdir in sorted(subdirs):
            check_dir(subdir, depth + 1)
    else:
        count = len(md_files)
        if count > 0:
            status = "✅" if count < MEDIUM else "⚠️" if count < LARGE else "🔴"
            rel = dir_path.relative_to(garden_dir)
            print(f"{indent}{status} {dir_path.name}: {count} notes")

            if count >= MEDIUM:
                categories.append({
                    'name': str(rel).replace('\\', '/'),
                    'count': count,
                    'recommend_split': count >= MEDIUM
                })


for category_dir in sorted(garden_dir.iterdir()):
    if category_dir.is_dir() and not category_dir.name.startswith('.'):
        check_dir(category_dir)

# Summary
print("\n" + "=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)

if not categories:
    print(f"✅ All categories are within optimal size (< {MEDIUM} notes)")
else:
    print(f"⚠️ {len(categories)} category(ies) exceed threshold:\n")
    for cat in categories:
        print(f"  🔍 {cat['name']}: {cat['count']} notes")
        print(f"     → Recommend subdivision into 2-3 subcategories")
        print()
