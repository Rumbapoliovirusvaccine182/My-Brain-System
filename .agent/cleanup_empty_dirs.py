"""
Clean up empty directories in the Garden.
Optionally deletes topic indices first (use --with-indices flag).
"""
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import config

garden_path = config.GARDEN_DIR

# Check for --with-indices flag
delete_indices = '--with-indices' in sys.argv

if delete_indices:
    deleted_indices = 0
    for f in garden_path.rglob("*_主題索引.md"):
        f.unlink()
        deleted_indices += 1
    print(f"Deleted {deleted_indices} topic indices.")

# Delete empty directories (multi-pass)
deleted_any = True
iter_count = 0
while deleted_any and iter_count < 10:
    deleted_any = False
    iter_count += 1
    for d in sorted(garden_path.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
            print(f"Removed empty directory: {d.relative_to(config.BRAIN_ROOT)}")
            deleted_any = True
