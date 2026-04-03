"""
Validate that taxonomy.md definitions match the actual 10_Garden/ folder structure.
Catches drift: folders without taxonomy entries, taxonomy entries without folders.
"""
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config
from utils.taxonomy_loader import load_taxonomy


def collect_taxonomy_paths(taxonomy: dict, prefix: str = "") -> set:
    """Recursively collect all category/subcategory paths from taxonomy."""
    paths = set()
    for name, defn in taxonomy.items():
        full = f"{prefix}/{name}" if prefix else name
        paths.add(full)
        subcats = defn.get('subcategories', {})
        if subcats:
            paths |= collect_taxonomy_paths(subcats, full)
    return paths


def collect_filesystem_paths(garden_dir: Path) -> set:
    """Collect all directory paths under Garden (relative)."""
    paths = set()
    for d in garden_dir.rglob("*"):
        if d.is_dir() and not d.name.startswith('.'):
            rel = str(d.relative_to(garden_dir)).replace('\\', '/')
            paths.add(rel)
    return paths


def validate():
    taxonomy = load_taxonomy()
    tax_paths = collect_taxonomy_paths(taxonomy)
    fs_paths = collect_filesystem_paths(config.GARDEN_DIR)

    # Folders that exist on disk but are not defined in taxonomy
    untracked = sorted(fs_paths - tax_paths)
    # Taxonomy entries that have no corresponding folder
    missing_dirs = sorted(tax_paths - fs_paths)

    print("=" * 70)
    print("TAXONOMY ↔ FILESYSTEM VALIDATION")
    print("=" * 70)

    if untracked:
        print(f"\n⚠️  Folders on disk NOT in taxonomy.md ({len(untracked)}):")
        for p in untracked:
            print(f"  + {p}")
    else:
        print("\n✅ All folders on disk are covered by taxonomy.md")

    if missing_dirs:
        print(f"\n⚠️  Taxonomy entries with NO folder on disk ({len(missing_dirs)}):")
        for p in missing_dirs:
            print(f"  - {p}")
    else:
        print("\n✅ All taxonomy entries have matching folders")

    if not untracked and not missing_dirs:
        print("\n🎯 Taxonomy and filesystem are perfectly in sync.")

    print()
    return untracked, missing_dirs


if __name__ == "__main__":
    validate()
