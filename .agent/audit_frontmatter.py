"""
Audit markdown files for missing YAML frontmatter.
"""
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config

missing_frontmatter = []
total_md = 0

for md_file in config.GARDEN_DIR.rglob("*.md"):
    total_md += 1
    try:
        first_line = md_file.read_text(encoding='utf-8').split('\n', 1)[0]
        if not first_line.startswith('---'):
            missing_frontmatter.append(md_file)
    except Exception:
        pass

print("--- Markdown Files Missing YAML Frontmatter ---")
for f in missing_frontmatter:
    print(f.relative_to(config.BRAIN_ROOT))

print("-" * 50)
print(f"Total MD files checked: {total_md}")
print(f"Total missing frontmatter: {len(missing_frontmatter)}")
