"""
Two-Tier Topic Index Generator for the Garden.

Tier 1 (Parent): Lightweight routing index (~500-800 tokens) for folders with subfolders.
Tier 2 (Leaf):   Compact table index (~3-8KB) for leaf folders with no subfolders.

Usage:
    python generate_indices.py              # Regenerate all indices
    python generate_indices.py AI_Hardware   # Regenerate indices for one category
    python generate_indices.py --clean-only  # Just delete stale indices
"""
import sys
import re
from pathlib import Path
from datetime import datetime

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config
from utils.markdown_parser import parse_note, extract_summary


def is_index_file(path: Path) -> bool:
    """Check if a file is a topic index."""
    return config.is_topic_index(path.name)


def is_leaf_folder(dir_path: Path) -> bool:
    """A leaf folder has no subdirectories (ignoring hidden dirs)."""
    return not any(d.is_dir() and not d.name.startswith('.') for d in dir_path.iterdir())


def get_notes(dir_path: Path) -> list:
    """Get all non-index .md files in a directory (non-recursive)."""
    notes = []
    for f in sorted(dir_path.glob('*.md')):
        if is_index_file(f):
            continue
        if f.name in config.EXCLUDE_FILES:
            continue
        if f.name.startswith('_'):
            continue
        try:
            meta = parse_note(f)
            summary = extract_summary(f.read_text(encoding='utf-8'))
            notes.append({
                'title': meta.title,
                'filename': meta.filename,
                'tags': meta.tags,
                'wikilinks': meta.wikilinks,
                'updated': meta.updated or '',
                'summary': summary or '',
            })
        except Exception as e:
            print(f"  Warning: could not parse {f.name}: {e}")
    return notes


def count_notes_recursive(dir_path: Path) -> int:
    """Count all non-index .md files recursively."""
    count = 0
    for f in dir_path.rglob('*.md'):
        if is_index_file(f) or f.name in config.EXCLUDE_FILES or f.name.startswith('_'):
            continue
        count += 1
    return count


def load_taxonomy_descriptions() -> dict:
    """Load category/subcategory descriptions from taxonomy.md."""
    descriptions = {}
    taxonomy_path = config.AGENT_DIR / 'taxonomy.md'
    if not taxonomy_path.exists():
        return descriptions

    content = taxonomy_path.read_text(encoding='utf-8')
    # Match ## Category or ### Category/Subcategory followed by **Description**: ...
    # Parse section by section
    current_key = None
    for line in content.splitlines():
        # Top-level: ## AI_Hardware
        m = re.match(r'^##\s+(\w+)\s*$', line)
        if m:
            current_key = m.group(1)
            continue
        # Subcategory: ### AI_Hardware/Compute
        m = re.match(r'^###\s+\w+/(\w+)\s*$', line)
        if m:
            current_key = m.group(1)
            continue
        # Description line
        m = re.match(r'^\*\*Description\*\*:\s*(.+)', line)
        if m and current_key:
            descriptions[current_key] = m.group(1).strip()

    return descriptions


# ============================================================================
# Step 1: Clean stale indices
# ============================================================================

def clean_stale_indices(root: Path) -> int:
    """Delete all index files whose name doesn't match their folder. Returns count deleted."""
    deleted = 0
    for idx_file in root.rglob('*主題索引*'):
        if not idx_file.is_file():
            continue
        expected_name = f"{idx_file.parent.name}_主題索引.md"
        if idx_file.name != expected_name:
            print(f"  [DEL] Stale index: {idx_file.relative_to(root)} (expected {expected_name})")
            idx_file.unlink()
            deleted += 1
    return deleted


# ============================================================================
# Step 2: Generate Tier 2 — Leaf indices (compact table)
# ============================================================================

def truncate(text: str, max_len: int = 80) -> str:
    """Truncate text to max_len, adding ellipsis."""
    text = text.replace('\n', ' ').strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 1] + '…'


def extract_key_entities(note: dict) -> str:
    """Extract key companies/concepts from tags and wikilinks."""
    entities = set()
    for tag in note.get('tags', []):
        # Skip generic category tags
        if tag in config.CATEGORIES:
            continue
        entities.add(tag)
    # Add first few wikilinks as entities
    for link in note.get('wikilinks', [])[:5]:
        # Skip index links and long paths
        if '主題索引' in link or '/' in link:
            continue
        entities.add(link)
    # Keep it compact
    return ', '.join(sorted(entities)[:3])


def generate_leaf_index(dir_path: Path, descriptions: dict) -> str:
    """Generate a Tier 2 compact table index for a leaf folder."""
    folder_name = dir_path.name
    notes = get_notes(dir_path)
    desc = descriptions.get(folder_name, '')

    lines = [
        '---',
        'type: index',
        f'scope: {folder_name}',
        f'updated: {datetime.now().strftime("%Y-%m-%d")}',
        f'total_notes: {len(notes)}',
        '---',
        '',
        f'# {folder_name} 主題索引',
        '',
        '## Overview',
        desc if desc else f'{folder_name} 相關筆記索引。',
        '',
    ]

    if not notes:
        lines.append('*尚無筆記*')
        return '\n'.join(lines)

    # Group notes into thematic clusters by first tag
    clusters = {}
    ungrouped = []
    for note in notes:
        # Use first non-category tag as cluster key
        cluster_key = None
        for tag in note['tags']:
            if tag not in config.CATEGORIES:
                cluster_key = tag
                break
        if cluster_key:
            clusters.setdefault(cluster_key, []).append(note)
        else:
            ungrouped.append(note)

    # If clustering produced too many tiny groups, merge into one
    if len(clusters) > 8 or (len(clusters) > 0 and all(len(v) == 1 for v in clusters.values())):
        ungrouped = notes
        clusters = {}

    lines.append('## Notes')
    lines.append('')

    def write_table(note_list):
        table_lines = []
        table_lines.append('| Note | Key Thesis | Companies/Concepts |')
        table_lines.append('|------|-----------|-------------------|')
        for n in sorted(note_list, key=lambda x: x['title']):
            thesis = truncate(n['summary'], 45) if n['summary'] else '—'
            entities = extract_key_entities(n) or '—'
            table_lines.append(f'| [[{n["title"]}]] | {thesis} | {entities} |')
        return table_lines

    if clusters:
        for cluster_name, cluster_notes in sorted(clusters.items()):
            lines.append(f'### {cluster_name}')
            lines.extend(write_table(cluster_notes))
            lines.append('')
        if ungrouped:
            lines.append('### 其他')
            lines.extend(write_table(ungrouped))
            lines.append('')
    else:
        lines.extend(write_table(ungrouped if ungrouped else notes))
        lines.append('')

    # Open questions placeholder
    lines.append('## Open Questions')
    lines.append('- (auto-generated index — review and add open questions manually)')
    lines.append('')

    return '\n'.join(lines)


# ============================================================================
# Step 3: Generate Tier 1 — Parent routing indices
# ============================================================================

def generate_parent_index(dir_path: Path, descriptions: dict) -> str:
    """Generate a Tier 1 lightweight routing index for a parent folder."""
    folder_name = dir_path.name
    subdirs = sorted([d for d in dir_path.iterdir() if d.is_dir()])
    total = count_notes_recursive(dir_path)

    lines = [
        '---',
        'type: index',
        f'scope: {folder_name}',
        f'updated: {datetime.now().strftime("%Y-%m-%d")}',
        f'total_notes: {total}',
        '---',
        '',
        f'# {folder_name} — Routing Index',
        '',
        '> **For agents**: Read this first to identify the relevant subcategory, then follow the WikiLink to the detailed index inside that folder.',
        '',
        '## Subcategories',
        '',
    ]

    for subdir in subdirs:
        sub_name = subdir.name
        sub_count = count_notes_recursive(subdir)
        sub_desc = descriptions.get(sub_name, f'{sub_name} 相關筆記。')
        index_link = f'{sub_name}/{sub_name}_主題索引|{sub_name}'
        lines.append(f'### [[{index_link}]] ({sub_count} notes)')
        lines.append(sub_desc)
        lines.append('')

    # Direct notes in parent (shouldn't be many)
    direct_notes = get_notes(dir_path)
    if direct_notes:
        lines.append('## Direct Notes (needs routing)')
        lines.append('')
        for n in direct_notes:
            lines.append(f'- [[{n["title"]}]]')
        lines.append('')

    # Cross-category connections
    lines.append('## Cross-Category Connections')
    lines.append('(Review subcategory indices for specific cross-links.)')
    lines.append('')

    return '\n'.join(lines)


# ============================================================================
# Main orchestration
# ============================================================================

def generate_for_directory(dir_path: Path, descriptions: dict):
    """Generate the appropriate index for a single directory."""
    folder_name = dir_path.name
    index_path = dir_path / f'{folder_name}_主題索引.md'

    # Delete existing index first
    if index_path.exists():
        index_path.unlink()

    if is_leaf_folder(dir_path):
        content = generate_leaf_index(dir_path, descriptions)
        kind = 'Tier 2 (leaf)'
    else:
        content = generate_parent_index(dir_path, descriptions)
        kind = 'Tier 1 (parent)'

    index_path.write_text(content, encoding='utf-8')
    size_kb = len(content.encode('utf-8')) / 1024
    print(f"  [{kind}] {index_path.relative_to(config.GARDEN_DIR)} ({size_kb:.1f} KB)")

    # Warn if parent index exceeds 3KB
    if not is_leaf_folder(dir_path) and size_kb > 3.0:
        print(f"    ⚠ Parent index exceeds 3KB target ({size_kb:.1f} KB)")


def generate_all(scope: str = None):
    """Generate all indices, optionally scoped to one top-level category."""
    print('=' * 60)
    print('Two-Tier Index Generator')
    print('=' * 60)

    descriptions = load_taxonomy_descriptions()

    # Step 1: Clean stale indices
    print('\nStep 1: Cleaning stale indices...')
    deleted = clean_stale_indices(config.GARDEN_DIR)
    print(f'  Deleted {deleted} stale index files.\n')

    # Determine scope
    if scope:
        targets = [config.GARDEN_DIR / scope]
        if not targets[0].exists():
            print(f'ERROR: {scope} not found in Garden.')
            sys.exit(1)
    else:
        targets = sorted([d for d in config.GARDEN_DIR.iterdir()
                          if d.is_dir() and not d.name.startswith('.')])

    # Step 2: Generate leaf indices (bottom-up)
    print('Step 2: Generating Tier 2 (leaf) indices...')
    for top_dir in targets:
        for subdir in sorted(top_dir.rglob('*')):
            if subdir.is_dir() and is_leaf_folder(subdir):
                generate_for_directory(subdir, descriptions)
        # Top-level is also a leaf if it has no subdirs
        if is_leaf_folder(top_dir):
            generate_for_directory(top_dir, descriptions)

    # Step 3: Generate parent indices (top-down)
    print('\nStep 3: Generating Tier 1 (parent) indices...')
    for top_dir in targets:
        if not is_leaf_folder(top_dir):
            generate_for_directory(top_dir, descriptions)
            # Any intermediate parents
            for subdir in sorted(top_dir.rglob('*')):
                if subdir.is_dir() and not is_leaf_folder(subdir):
                    generate_for_directory(subdir, descriptions)

    # Step 4: Verify
    print('\nStep 4: Verification...')
    issues = 0
    for d in config.GARDEN_DIR.rglob('*'):
        if not d.is_dir():
            continue
        if d == config.GARDEN_DIR:
            continue
        # Skip hidden directories (.obsidian, etc.)
        if any(part.startswith('.') for part in d.relative_to(config.GARDEN_DIR).parts):
            continue
        expected = d / f'{d.name}_主題索引.md'
        if not expected.exists():
            print(f'  ⚠ Missing index: {d.relative_to(config.GARDEN_DIR)}/')
            issues += 1

    if issues == 0:
        print('  ✓ All directories have correctly-named indices.')
    else:
        print(f'  {issues} issue(s) found.')

    print('\n' + '=' * 60)
    print('✓ Index generation complete.')
    print('=' * 60)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--clean-only':
            deleted = clean_stale_indices(config.GARDEN_DIR)
            print(f'Deleted {deleted} stale index files.')
        else:
            generate_all(scope=arg)
    else:
        generate_all()
