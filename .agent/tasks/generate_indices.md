# Task: Generate Two-Tier Topic Indices
# Trigger: `@Agent Update Indexes`, after `Sort Garden`, or after bulk ingest (10+ notes)

## Architecture: Two-Tier Index System

The Garden uses a **two-tier index system** optimized for both human browsing and agent lookup:

### Tier 1: Parent Routing Index (lightweight, ~500-800 tokens)
- **Purpose**: Help an agent or reader quickly decide which subcategory to drill into
- **Location**: Every folder that HAS child subfolders (e.g., `AI_Hardware/AI_Hardware_主題索引.md`)
- **Content**: Subcategory list with note counts, 2-3 sentence descriptions, WikiLinks to child indices, cross-category connections
- **Size target**: Under 3KB. If it exceeds this, it's too detailed — push detail down to Tier 2
- **Never contains**: Individual note summaries (that's Tier 2's job)

### Tier 2: Leaf Detail Index (comprehensive, per-note summaries)
- **Purpose**: Provide detailed knowledge map for a specific subcategory
- **Location**: Every leaf folder (no child subfolders) (e.g., `AI_Hardware/Compute/Compute_主題索引.md`)
- **Content**: Executive summary, notes grouped by theme with summaries and key insights, actionable next steps
- **Size**: Proportional to note count (~1KB per note)

## Critical Rules

1. **One index per folder**: Each folder gets exactly one `[FolderName]_主題索引.md`. No duplicates, no legacy names.
2. **Index name MUST match folder name**: `Compute/` → `Compute_主題索引.md`. Never `NVIDIA_Ecosystem_主題索引.md` inside `Compute/`.
3. **Delete before regenerate**: Before writing any index, delete ALL `*主題索引*` files in that folder first. This prevents stale indices from accumulating after restructures.
4. **Parent vs Leaf detection**: A folder with subdirectories = Parent (Tier 1). A folder without subdirectories = Leaf (Tier 2).

## Process

### Step 1: Clean Stale Indices
Walk ALL folders in `10_Garden/` recursively. For each `*主題索引*` file found:
- If its name doesn't match the folder it's in → **delete it** (stale from old structure)

### Step 2: Generate Leaf Indices (Tier 2)
For each leaf folder (no subdirectories):

1. **Scan**: Read all `.md` files in the folder (excluding index files and files starting with `_`)
2. **Synthesize**: Identify core themes, group notes into 2-5 thematic clusters
3. **Generate**: Write `[FolderName]_主題索引.md` in **compact table format**:

```markdown
---
type: index
scope: [folder_name]
updated: [today]
total_notes: [N]
---

# [Folder Name] 主題索引

## Overview
[3-5 sentence synthesis of what this subcategory covers, key themes, current state of knowledge]

## Thematic Groups

### [Theme A]
| Note | Key Thesis | Companies/Concepts |
|------|-----------|-------------------|
| [[Note Title]] | One-sentence thesis (under 20 words) | Key entities |
| [[Note Title]] | One-sentence thesis | Key entities |

### [Theme B]
| Note | Key Thesis | Companies/Concepts |
|------|-----------|-------------------|
| ... | ... | ... |

## Open Questions
- [1-2 knowledge gaps or unresolved debates]
```

**Leaf index rules**:
- Each note gets ONE table row — no multi-paragraph summaries (the full summary lives inside the note itself)
- "Key Thesis" = the single most important claim or insight, under 20 words
- "Companies/Concepts" = key entities for agent keyword matching
- Group into 2-5 thematic clusters (not alphabetical, not by legacy tags)
- **Size target: 3-8KB** (roughly 100-250 bytes per note). If over 8KB, it's too verbose — shorten theses

### Step 3: Generate Parent Indices (Tier 1)
For each parent folder (has subdirectories):

1. **Scan**: Read the Tier 2 index of each child folder (NOT individual notes)
2. **Count**: Note count per child
3. **Generate**: Write `[FolderName]_主題索引.md` with this structure:

```markdown
---
type: index
scope: [folder_name]
updated: [today]
total_notes: [N across all children]
---

# [Folder Name] — Routing Index

> **For agents**: Read this first to identify the relevant subcategory, then follow the WikiLink to the detailed index inside that folder.

## Subcategories

### [[Child_A/Child_A_主題索引|Child_A]] (N notes)
[2-3 sentence description of coverage. Key companies, technologies, or themes.]

### [[Child_B/Child_B_主題索引|Child_B]] (N notes)
[2-3 sentence description.]

## Cross-Category Connections
[How this category connects to other top-level categories. Which WikiLinks bridge domains.]
```

**Size check**: Parent index must be under 3KB. If over, it's too detailed.

### Step 4: Verify
After all indices are generated:
- Every folder should have exactly one `[FolderName]_主題索引.md`
- No orphaned indices from old names
- Parent indices under 3KB
- Leaf indices contain all notes in their folder

## Constraints
- Language: Traditional Chinese with English technical terms
- Use `[[WikiLinks]]` for all note references
- Do NOT list index files in the knowledge map
- Do NOT include notes starting with `_` in the index
