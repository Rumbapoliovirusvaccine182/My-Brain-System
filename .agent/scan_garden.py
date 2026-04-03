"""
Scan Garden notes and generate statistics report for restructuring analysis.
"""
import sys
import re
import json
from collections import Counter, defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config

garden_path = config.GARDEN_DIR

data = []
all_tags = []
tag_counts = defaultdict(Counter)

for root_dir in garden_path.rglob("*.md"):
    file = root_dir
    if file.name.endswith("_主題索引.md") or file.name == "taxonomy.md":
        continue

    content = file.read_text(encoding='utf-8')

    # Parse frontmatter
    frontmatter = {}
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        for line in fm_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                if key.strip() == 'title':
                    frontmatter['title'] = val.strip()
                elif key.strip() == 'tags':
                    tags_match = re.search(r'\[(.*?)\]', val)
                    if tags_match:
                        tags = [t.strip() for t in tags_match.group(1).split(',')]
                        frontmatter['tags'] = tags

    # Extract wikilinks
    wikilinks = re.findall(r'\[\[(.*?)\]\]', content)

    rel_dir = str(file.parent.relative_to(garden_path)).replace('\\', '/')

    item = {
        "file": file.name,
        "category": rel_dir,
        "title": frontmatter.get('title', file.stem),
        "tags": frontmatter.get('tags', []),
        "wikilinks": wikilinks
    }
    data.append(item)

    if rel_dir.startswith("Investment"):
        for tag in item['tags']:
            if tag not in ["Investment", "Investment_Frameworks", "Industry_Analysis", "Geopolitics_Macro"]:
                tag_counts[rel_dir][tag] += 1

report = {
    "total_files": len(data),
    "category_counts": dict(Counter([item['category'] for item in data])),
    "tag_clusters": {k: dict(v.most_common(15)) for k, v in tag_counts.items()}
}

output_path = config.AGENT_DIR / "garden_scan_report.json"
with open(output_path, 'w', encoding='utf-8') as out:
    json.dump(report, out, ensure_ascii=False, indent=2)

print(f"Scan complete. {len(data)} notes analyzed. Report saved to {output_path.name}")
