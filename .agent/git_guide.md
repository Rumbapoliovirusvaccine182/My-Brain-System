# Git Version Control Guide for My Brain

## Overview

Your knowledge base is now under Git version control, enabling you to:
- Track all changes to your notes and organization
- Rollback to previous states if needed
- View history of modifications
- Create branches for experimental reorganizations

## Current Status

✅ **Git initialized** and configured  
✅ **Initial commit created** (commit hash: `7929712`)  
✅ **.gitignore configured** to exclude temporary files

**Latest Commit**:
```
7929712 feat: Garden reorganization and topic index enhancement
```

This commit includes:
- Investment category reorganization (4 subcategories)
- All 17 topic indices enhanced with summaries
- 6 files ingested and archived
- Taxonomy v2.1 updates
- Topic index specification

---

## Common Git Commands

### View History
```bash
# View recent commits
git log --oneline -10

# View detailed history
git log

# View changes in a specific commit
git show <commit-hash>
```

### Check Status
```bash
# See what files have changed
git status

# See detailed changes
git diff
```

### Save Changes
```bash
# Stage all changes
git add -A

# Stage specific files
git add <file-path>

# Commit with message
git commit -m "Your descriptive message"

# Quick commit of all changes
git commit -am "Your message"
```

### Rollback Changes

#### Undo uncommitted changes
```bash
# Discard changes to a specific file
git checkout -- <file-path>

# Discard all uncommitted changes (CAREFUL!)
git reset --hard HEAD
```

#### Rollback to previous commit
```bash
# View commit history to find the commit you want
git log --oneline

# Rollback to a specific commit (keeps changes as uncommitted)
git reset <commit-hash>

# Rollback and discard all changes (CAREFUL!)
git reset --hard <commit-hash>
```

#### Undo last commit (keep changes)
```bash
git reset --soft HEAD~1
```

---

## Recommended Workflow

### After Making Changes

1. **Check what changed**:
   ```bash
   git status
   git diff
   ```

2. **Stage and commit**:
   ```bash
   git add -A
   git commit -m "Brief description of changes"
   ```

### Before Major Reorganizations

1. **Ensure current work is committed**:
   ```bash
   git status  # Should show "nothing to commit, working tree clean"
   ```

2. **Create a backup branch** (optional):
   ```bash
   git branch backup-before-reorganization
   ```

3. **Make your changes**

4. **Commit the reorganization**:
   ```bash
   git add -A
   git commit -m "Reorganized [category] structure"
   ```

### If Something Goes Wrong

1. **Find the last good commit**:
   ```bash
   git log --oneline
   ```

2. **Rollback to that commit**:
   ```bash
   git reset --hard <commit-hash>
   ```

---

## Commit Message Best Practices

Use descriptive commit messages following this format:

```
<type>: <brief description>

<optional detailed explanation>
```

**Types**:
- `feat`: New feature or major addition
- `fix`: Bug fix or correction
- `refactor`: Reorganization or restructuring
- `docs`: Documentation updates
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat: Add new Investment subcategory for ESG analysis"
git commit -m "refactor: Reorganize AI_Tech notes by application domain"
git commit -m "fix: Correct broken WikiLinks in NVIDIA_Ecosystem index"
git commit -m "docs: Update topic index specification with new examples"
```

---

## Important Notes

### What's Tracked
- ✅ All markdown notes (`*.md`)
- ✅ Python scripts (`.agent/*.py`)
- ✅ Configuration files (`taxonomy.md`, `config.py`)
- ✅ Archived assets (`99_Archives/Assets/*`)

### What's Ignored (via .gitignore)
- ❌ Temporary files (`*.tmp`, `*.bak`)
- ❌ Google Drive sync files (`.tmp.driveupload/`)
- ❌ Python cache (`__pycache__/`)
- ❌ Antigravity session artifacts (`.gemini/`)

### Binary Files
Currently, binary files (PDFs, images) **are tracked**. If your repository becomes too large, you can:

1. **Exclude future binary files**: Uncomment lines in `.gitignore`:
   ```gitignore
   *.pdf
   *.jpg
   *.jpeg
   *.png
   ```

2. **Remove existing binary files from tracking** (keeps files, just stops tracking):
   ```bash
   git rm --cached 99_Archives/Assets/*.pdf
   git commit -m "Stop tracking PDF files"
   ```

---

## Quick Reference

| Task | Command |
|------|---------|
| View status | `git status` |
| View history | `git log --oneline -10` |
| Save all changes | `git add -A && git commit -m "message"` |
| Undo uncommitted changes | `git reset --hard HEAD` |
| Rollback to commit | `git reset --hard <hash>` |
| View specific commit | `git show <hash>` |

---

## Safety Tips

1. **Always check status before committing**:
   ```bash
   git status
   ```

2. **Review changes before committing**:
   ```bash
   git diff
   ```

3. **Use descriptive commit messages** - your future self will thank you

4. **Commit frequently** - smaller commits are easier to understand and rollback

5. **Before using `--hard` flag**, make sure you really want to discard changes

---

## Next Steps

1. **Commit regularly** after making significant changes
2. **Review commit history** periodically to understand your knowledge evolution
3. **Consider remote backup** (GitHub, GitLab) for additional safety

For more Git commands and advanced usage, see: https://git-scm.com/docs
