# Task: Sort Garden — Dynamic Taxonomy Evolution
# Trigger: User says "Sort Garden" or "Restructure Garden"

> **Core Loop**: `taxonomy.md` is **read** at the start (as the current basis) and **rewritten** at the end (as the evolved basis). Each sort cycle evolves the taxonomy, which then governs the next ingest or sort.

> [!IMPORTANT]
> **Scope**: This workflow analyzes **ALL** categories in `10_Garden` — not just one.
> The folder structure is **fully dynamic**: categories can be created, deleted, merged, promoted, demoted, or rearranged at any level based on content analysis.

---

# Structural Principles (MANDATORY — apply at every sort cycle)

These principles govern ALL structural decisions. They are non-negotiable and must be evaluated before proposing any changes.

## 1. MECE (Mutually Exclusive, Collectively Exhaustive)
- **At each level**, sibling folders must not overlap in scope. A note should have exactly one correct home.
- **Collectively**, siblings must cover all notes that belong under their parent. No orphans.
- **Test**: If you can't decide between two siblings for a note, the categories are not mutually exclusive → redefine boundaries.

## 2. Pyramid Structure
- **Max 3 levels of nesting**: `Top Category > Subcategory > [note]`. A 4th level is only acceptable temporarily when a subcategory is actively being subdivided.
- **3-8 children per parent**: Fewer than 3 = merge with sibling or promote children. More than 8 = too broad, needs an intermediate grouping.
- **Balanced sizing**: Siblings should be within 5:1 note count ratio. A 15:1 ratio signals a structural problem — the large sibling likely deserves promotion or the small one should merge.

## 3. No Phantom Parents
- A folder that contains ≤2 notes of its own but exists only as a routing layer to children is a **phantom parent**. Eliminate by either:
  - Promoting children to the parent's level, or
  - Absorbing parent content into children.

## 4. Leaf Folder Sizing
- **Target**: 5-20 notes per leaf folder (navigable, scannable)
- **>20 notes**: Evaluate for subdivision
- **>30 notes**: Strongly recommend subdivision
- **<3 notes**: Merge into nearest sibling or parent

## 5. Top-Level Categories Reflect the User's Mental Model
- Top-level should map to how the user **thinks about** their knowledge, not academic taxonomy.
- A top-level category containing >80% of all notes is not a category — it's a filing cabinet. Split it.
- Top-level count target: 5-8 categories for a system of this size.

## 6. Evolution Over Perfection
- Each sort cycle should make **incremental improvements**, not perfect the structure in one pass.
- When in doubt between two valid structures, prefer the one that **minimizes depth** and **maximizes MECE clarity**.
- The structure should feel natural for the user to navigate in Obsidian's file explorer.

---

# Phase 1: Scan & Cluster

**Objective**: Understand what's actually in the Garden right now and evaluate structural health.

1. **Load Current Taxonomy**: Read `.agent/taxonomy.md` as the baseline.
2. **Structural Health Check** (apply Structural Principles above):
   - Measure: max depth, notes per leaf, sibling ratios, phantom parents, top-level concentration
   - Flag any violations of the 6 principles
3. **Scan All Files**: Read every `.md` file in `10_Garden/` recursively (excluding `*_主題索引.md` index files).
   - For each note, extract: Title, tags, frontmatter, content themes, WikiLinks, current location
4. **Build Content Map**: Group notes by semantic similarity:
   - What topics cluster together?
   - Which notes link to each other heavily? (wikilink affinity)
   - Are there emerging themes NOT captured by current taxonomy?
   - Are there categories that are too thin or should be merged?
5. **Compare to Current Structure**: Identify mismatches:
   - Files in the wrong category
   - Structural principle violations requiring folder-level changes (promotions, merges, splits)
   - Missing categories for emerging themes
   - Obsolete categories with ≤2 files

**Output**: Internal analysis — no user-facing artifact yet.

---

# Phase 2: Propose Reorganization

**Objective**: Present a clear, diff-style proposal to the user.

Create a reorganization proposal showing:

```markdown
# 🌱 Garden Reorganization Proposal

## Summary
- Total notes analyzed: N
- Changes proposed: M file moves, X new folders, Y folder deletions

## Structure Changes

### [Category Name]
**Status**: [Keep / Rename to X / Merge with Y / NEW / DELETE]
**Current**: X files in N subfolders
**Proposed**: Y files in M subfolders

#### Moves:
- `Note_A.md`: AI_Tech → Investment/Industry_Analysis (reason: primarily about investment thesis)
- `Note_B.md`: General → AI_Tech/AI_Applications (reason: content is about AI agents)

#### New Subcategories:
- `[NewSubcat]/` — N files, description: ...

#### Subcategories to Remove:
- `[OldSubcat]/` — merge remaining files into [Target]

---

## Taxonomy Changes Preview
- **New keywords added**: [list]
- **New categories/subcategories**: [list]
- **Removed categories**: [list]
```

**Constraints**:
- DO NOT move any files yet — only create the proposal
- All proposals MUST satisfy the Structural Principles defined above (MECE, Pyramid, no phantoms, balanced sizing, leaf targets, mental model alignment)
- Structural changes (promotions, merges, depth reduction) take priority over simple note moves
- Include a "Structural Health" section showing before/after metrics: max depth, top-level count, largest leaf, smallest leaf, phantom parents

**Wait for user approval before proceeding.**

---

# Phase 3: Execute Moves

**Objective**: Restructure the Garden per the approved plan.

1. **Create New Directories**: Make any new category/subcategory folders.
2. **Move Files**: Relocate notes according to the approved mapping.
3. **Update WikiLinks**: For each moved file, search all other Garden files for WikiLinks pointing to it. Update the paths if the WikiLink uses a relative path. (Obsidian-style `[[name]]` links without paths do NOT need updating.)
4. **Clean Up**: Delete any empty directories left behind.
5. **Regenerate ALL Indices** (MANDATORY after any structural change):
   Run `python .agent/generate_indices.py` (no arguments = full regeneration). This:
   - Deletes ALL stale `*主題索引*` files whose names don't match their folder
   - Regenerates Tier 2 (leaf compact table indices) for every leaf folder
   - Regenerates Tier 1 (parent routing indices) for every parent folder
   - Verifies every folder has exactly one correctly-named index, parents under 3KB

   > **Why this matters**: Stale indices from old folder names accumulate after restructures and confuse external agents (Project Wealth) that scan the Garden.

---

# Phase 4: Evolve Taxonomy

**Objective**: Rewrite `taxonomy.md` to reflect the new reality. This is the critical feedback loop.

> [!IMPORTANT]
> **This is NOT a patch**. Regenerate `taxonomy.md` from the actual current structure.
> The evolved taxonomy becomes the starting point for the **next** `sort garden` or `ingest` run.

1. **Scan the new `10_Garden/` structure** to discover all categories and subcategories that now exist.
2. **For each category/subcategory**, write:
   - `**Description**`: What this folder contains (derived from actual content, not guessed)
   - `**Keywords**`: Extract representative keywords from the notes in this folder — include both English and Chinese terms
3. **Preserve the structural format** exactly so `taxonomy_loader.py` can still parse it:
   - `## Category` for top-level
   - `### Subcategory` for level 2
   - `#### Category/Subcategory` for level 3+
   - `**Keywords**:` on a single line, comma-separated
4. **Preserve the Usage Guidelines section** at the bottom (Categorization Rules, Threshold Guidelines, etc.)
5. **Update the footer metadata**:
   - `**Last Updated**`: today's date
   - `**Version**`: increment by 0.1
   - `**Last Sort Summary**`: one-line description of what changed this cycle (e.g., "Added Space_Industry subcategory under Investment, merged General into other categories")

**Quality Checklist before saving taxonomy.md**:
- [ ] Every folder in `10_Garden/` has a matching entry in taxonomy.md
- [ ] Every entry in taxonomy.md has a matching folder in `10_Garden/`
- [ ] Keywords reflect actual note content, not just guesses
- [ ] New categories discovered during clustering are included
- [ ] Obsolete categories that were removed/merged are gone
- [ ] `taxonomy_loader.py` format is preserved (## / ### / #### headers, **Keywords**: line)

---

# Complete Execution Summary

When user says **"sort garden"**:

```
✓ Phase 1: Scan entire 10_Garden + load current taxonomy.md as baseline
✓ Phase 2: Propose reorganization → Wait for user approval
✓ Phase 3: Execute file moves, update wikilinks, regenerate indices
✓ Phase 4: Evolve taxonomy.md → becomes basis for next cycle
```

**The Feedback Loop**:
```
taxonomy.md (v2.1) → guides Sort Garden analysis
    → Sort Garden discovers better structure
        → taxonomy.md (v2.2) written
            → next Ingest or Sort uses v2.2 as basis
```

---

# Quality Checklist (user_persona Compliance)

Before finalizing, verify:

- [ ] **Whole-Garden Scope**: Analyzed ALL categories, not just one
- [ ] **Knowledge Interconnection**: New structure facilitates cross-category WikiLinks
- [ ] **Strategic Relevance**: Categories aligned with consulting/investment value
- [ ] **Balanced Distribution**: Each leaf folder has 3–20 files
- [ ] **Taxonomy Evolved**: taxonomy.md fully reflects new structure
- [ ] **Indices Regenerated**: Two-tier index system fully rebuilt (stale deleted, leaves detailed, parents lightweight)
- [ ] **No Stale Indices**: Every `*主題索引*` file name matches its folder name
- [ ] **Parent Index Size**: All parent routing indices under 3KB
