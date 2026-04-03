"""
Check WikiLinks in all Garden notes to identify broken references.
Uses the unified wikilink_manager module.
"""
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config
from utils.wikilink_manager import check_wikilinks, get_link_stats


def main():
    print("[*] Scanning WikiLinks in Garden notes...\n")

    stats = get_link_stats(config.GARDEN_DIR, config.EXCLUDE_FILES)
    broken = check_wikilinks(config.GARDEN_DIR, config.EXCLUDE_FILES)

    print(f"[OK] Total WikiLinks: {stats['total_links']}")
    print(f"[X]  Broken links: {stats['broken_count']}")
    print(f"[!]  Notes with broken links: {stats['notes_with_broken']}")
    print(f"[~]  Orphan notes (0 links): {stats['orphan_count']}")

    if broken:
        print(f"\n{'=' * 70}")
        print("BROKEN LINKS REPORT")
        print(f"{'=' * 70}")
        for source, links in sorted(broken.items()):
            print(f"\n[FILE] {source}")
            for link in links:
                print(f"   [X] [[{link}]]")

    print(f"\n{'=' * 70}")
    print(f"Summary: {stats['total_notes']} notes, {stats['total_links']} links, {stats['broken_count']} broken")


if __name__ == "__main__":
    main()
