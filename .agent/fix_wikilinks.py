"""
Fix broken WikiLinks by removing dead links.
Uses the unified wikilink_manager module.

Usage:
    python fix_wikilinks.py           # Dry run (report only)
    python fix_wikilinks.py --apply   # Actually fix broken links
"""
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config
from utils.wikilink_manager import remove_dead_links, get_link_stats


def main():
    dry_run = '--apply' not in sys.argv

    if dry_run:
        print("[DRY RUN] Scanning for dead WikiLinks (use --apply to fix)...\n")
    else:
        print("[APPLY] Fixing dead WikiLinks...\n")

    removals = remove_dead_links(config.GARDEN_DIR, config.EXCLUDE_FILES, dry_run=dry_run)

    if removals:
        for r in removals:
            print(f"  {'[WOULD]' if dry_run else '[FIXED]'} {r}")
        print(f"\nTotal: {len(removals)} link(s) {'to fix' if dry_run else 'fixed'}")
    else:
        print("No dead links found to remove.")

    if dry_run and removals:
        print("\nRun with --apply to execute these fixes.")


if __name__ == "__main__":
    main()
