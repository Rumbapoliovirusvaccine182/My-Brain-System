"""
WikiLink integrity management for My Brain knowledge management system.
Unified tool for checking, fixing, and updating WikiLinks across the Garden.
"""
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from . import file_ops, markdown_parser


def scan_all_notes(garden_dir: Path, exclude: List[str] = None) -> Dict[str, Path]:
    """
    Build a lookup map of all note titles -> file paths in the Garden.

    Returns:
        Dict mapping note stem (filename without .md) to its Path
    """
    if exclude is None:
        exclude = []

    note_map = {}
    for md_file in garden_dir.rglob("*.md"):
        if md_file.name in exclude or md_file.name.endswith('_主題索引.md'):
            continue
        note_map[md_file.stem] = md_file
    return note_map


def check_wikilinks(garden_dir: Path, exclude: List[str] = None) -> Dict[str, List[str]]:
    """
    Check all WikiLinks and return broken ones.

    Returns:
        Dict mapping source file path (relative) to list of broken link targets
    """
    note_map = scan_all_notes(garden_dir, exclude)
    all_stems = set(note_map.keys())

    # Also include topic indices as valid targets
    for md_file in garden_dir.rglob("*_主題索引.md"):
        all_stems.add(md_file.stem)

    broken = defaultdict(list)

    for stem, path in note_map.items():
        content = file_ops.read_markdown(path)
        links = markdown_parser.extract_wikilinks(content)

        for link in links:
            # Normalize: strip path prefixes, get just the note name
            link_target = link.split('/')[-1] if '/' in link else link
            if link_target not in all_stems:
                rel = str(path.relative_to(garden_dir))
                broken[rel].append(link)

    return dict(broken)


def update_wikilinks_after_move(
    garden_dir: Path,
    moves: List[Tuple[str, str]],
    exclude: List[str] = None,
    dry_run: bool = False
) -> List[str]:
    """
    After files are moved, update WikiLinks across the entire Garden.

    Since Obsidian resolves [[Note Title]] by stem regardless of path,
    most links survive moves. This function handles cases where links
    use relative paths (e.g., [[../Category/Note]]) that break on move.

    Args:
        garden_dir: Path to Garden root
        moves: List of (old_stem, new_stem) tuples for renamed files
        exclude: Files to exclude from scanning
        dry_run: If True, report changes without writing

    Returns:
        List of change descriptions
    """
    if exclude is None:
        exclude = []

    changes = []

    # Build rename map
    rename_map = {old: new for old, new in moves if old != new}
    if not rename_map:
        return changes

    for md_file in garden_dir.rglob("*.md"):
        if md_file.name in exclude:
            continue

        content = file_ops.read_markdown(md_file)
        new_content = content

        for old_stem, new_stem in rename_map.items():
            # Replace [[old_stem]] with [[new_stem]]
            old_pattern = f"[[{old_stem}]]"
            new_pattern = f"[[{new_stem}]]"
            if old_pattern in new_content:
                new_content = new_content.replace(old_pattern, new_pattern)
                changes.append(f"{md_file.name}: [[{old_stem}]] -> [[{new_stem}]]")

            # Also handle [[path/old_stem]] and [[path/old_stem|display]]
            old_re = re.compile(r'\[\[([^\]]*/)?' + re.escape(old_stem) + r'(\|[^\]]+)?\]\]')
            def replace_fn(m):
                prefix = m.group(1) or ''
                display = m.group(2) or ''
                return f"[[{prefix}{new_stem}{display}]]"

            replaced = old_re.sub(replace_fn, new_content)
            if replaced != new_content:
                changes.append(f"{md_file.name}: path-link updated for {old_stem}")
                new_content = replaced

        if new_content != content and not dry_run:
            file_ops.write_markdown(md_file, new_content)

    return changes


def remove_dead_links(garden_dir: Path, exclude: List[str] = None, dry_run: bool = False) -> List[str]:
    """
    Find and remove WikiLinks that point to non-existent notes.

    Args:
        garden_dir: Path to Garden root
        exclude: Files to exclude
        dry_run: If True, report without writing

    Returns:
        List of removal descriptions
    """
    broken = check_wikilinks(garden_dir, exclude)
    removals = []

    for rel_path, dead_links in broken.items():
        full_path = garden_dir / rel_path
        if not full_path.exists():
            continue

        content = file_ops.read_markdown(full_path)
        new_content = content

        for link in dead_links:
            # Remove the WikiLink but keep display text if present
            # [[target|display]] -> display
            # [[target]] -> (removed)
            pattern_with_display = f"[[{link}|"
            if pattern_with_display in new_content:
                # Find full pattern and extract display text
                match = re.search(r'\[\[' + re.escape(link) + r'\|([^\]]+)\]\]', new_content)
                if match:
                    new_content = new_content.replace(match.group(0), match.group(1))
                    removals.append(f"{rel_path}: removed dead link [[{link}]], kept display text")
            else:
                # Patterns to try for clean removal (with surrounding punctuation)
                patterns = [
                    (f"- [[{link}]]", ""),           # Bullet list item
                    (f"[[{link}]]、", ""),             # Followed by Chinese comma
                    (f"、[[{link}]]", ""),             # Preceded by Chinese comma
                    (f"[[{link}]]，", ""),             # Followed by Chinese comma
                    (f"，[[{link}]]", ""),             # Preceded by Chinese comma
                    (f"[[{link}]]", ""),               # Standalone
                ]

                for old, new in patterns:
                    if old in new_content:
                        new_content = new_content.replace(old, new)
                        removals.append(f"{rel_path}: removed dead link [[{link}]]")
                        break

        if new_content != content and not dry_run:
            file_ops.write_markdown(full_path, new_content)

    return removals


def get_link_stats(garden_dir: Path, exclude: List[str] = None) -> Dict:
    """
    Generate WikiLink statistics for the Garden.

    Returns:
        Dict with total_links, broken_count, notes_with_broken, orphan_notes (0 outgoing links)
    """
    note_map = scan_all_notes(garden_dir, exclude)
    all_stems = set(note_map.keys())
    for md_file in garden_dir.rglob("*_主題索引.md"):
        all_stems.add(md_file.stem)

    total_links = 0
    broken_count = 0
    notes_with_broken = 0
    orphan_notes = []

    for stem, path in note_map.items():
        content = file_ops.read_markdown(path)
        links = markdown_parser.extract_wikilinks(content)
        total_links += len(links)

        if not links:
            orphan_notes.append(stem)

        has_broken = False
        for link in links:
            target = link.split('/')[-1] if '/' in link else link
            if target not in all_stems:
                broken_count += 1
                has_broken = True

        if has_broken:
            notes_with_broken += 1

    return {
        'total_links': total_links,
        'broken_count': broken_count,
        'notes_with_broken': notes_with_broken,
        'orphan_notes': orphan_notes,
        'orphan_count': len(orphan_notes),
        'total_notes': len(note_map),
    }
