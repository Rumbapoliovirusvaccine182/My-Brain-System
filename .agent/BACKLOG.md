# Knowledge System Backlog

> Improvement roadmap for transforming "My Brain" from a filing cabinet into a thinking partner.
> Created: 2026-03-24

---

## Phase 1: Clean the Machine _(structural hygiene)_

### 1.1 Delete Dead Migration Scripts
- **Status**: [x] Done (2026-03-24)
- **Effort**: Small
- **Description**: Remove 23 one-off migration/temp scripts that clutter `.agent/` and obscure actual infrastructure.
- **Scripts to delete**:
  - `migrate_frontmatter.py`, `migrate_frontmatter_v2.py`
  - `move_ai_hardware.py`, `move_semi_mfg.py`, `move_strays.py`
  - `execute_garden_moves.py`, `execute_deep_sort.py`, `execute_final_moves.py`
  - `temp_move.py`, `temp_move_11.py`, `temp_restructure.py`
  - `deploy_ai_tech_split.py`, `deploy_restructure.py`
  - `generate_proposal.py`, `generate_mappings.py`
  - `add_wikilinks.py`, `archive_files.py`, `rename_topic_indices.py`
  - `extract_pdf.py` (superseded by `process_inbox.py`)
  - `create_pdf_notes.py`, `make_notes.py`, `audit_garden.py`
  - `analyze_notes_quality.py`
- **Preserved core scripts**: `config.py`, `process_inbox.py`, `generate_indices.py`, `analyze_categorization.py`, `scan_garden.py`, `analyze_garden.py`, `check_wikilinks.py`, `fix_wikilinks.py`, `check_category_sizes.py`, `audit_frontmatter.py`, `cleanup_empty_dirs.py`

### 1.2 Reorganize Task Docs
- **Status**: [x] Done (2026-03-24)
- **Effort**: Small
- **Description**: Move `task_*.md` files into `.agent/tasks/` subfolder for cleaner separation of workflow definitions vs scripts.
- **Moves**:
  - `task_ingest.md` → `tasks/ingest.md`
  - `task_restructure_garden.md` → `tasks/restructure.md`
  - `task_auto_subdivide.md` → `tasks/subdivide.md`
  - `task_deploy_structure.md` → `tasks/deploy.md`
  - `task_generate_category_indices.md` → `tasks/generate_indices.md`
  - `task_update_dashboard.md` → `tasks/update_dashboard.md`
  - `task_creator.md` → `tasks/creator.md`
  - `topic_index_spec.md` → `tasks/topic_index_spec.md`
  - `workflow_auto_subdivision.md` → `tasks/workflow_auto_subdivision.md`
- **Update**: All cross-references in `system_instructions.md`, `README.md`, and within task files themselves.

### 1.3 Clean Generated Artifacts
- **Status**: [x] Done (2026-03-24)
- **Effort**: Small
- **Description**: Remove stale JSON reports, cache, and pycache that shouldn't be tracked.
- **Actions**:
  - Delete `garden_categorization.json`, `dashboard_analysis.json`, `garden_scan_report.json`
  - Delete `garden_restructure_report.md`, `wikilink_analysis.md`, `wikilink_report.txt`
  - Clear `.agent/cache/` and `.agent/__pycache__/`
  - Add cache/pycache patterns to `.gitignore`

---

## Phase 2: Strengthen the Foundation _(quality & maintainability)_

### 2.1 Add `updated` / `review_by` Metadata to All Notes
- **Status**: [x] Done (2026-03-24) — 207 notes updated, 3 skipped (indices)
- **Effort**: Small
- **Description**: Add `updated: YYYY-MM-DD` and `review_by: YYYY-MM-DD` (created + 6 months) to all 241 garden notes. Enables staleness detection — critical for an investor whose notes decay fast.
- **Implementation**: Batch script to parse frontmatter, inject fields, write back.

### 2.2 WikiLink Integrity System
- **Status**: [x] Done (2026-03-24) — Built `utils/wikilink_manager.py` with check, fix, update-after-move, stats. Rewired `check_wikilinks.py` and `fix_wikilinks.py` to use it.
- **Effort**: Medium
- **Description**: After any file move, auto-scan and repair broken `[[links]]`. Integrate into sort-garden workflow. Current `check_wikilinks.py` and `fix_wikilinks.py` exist but aren't wired into any workflow.
- **Deliverable**: Unified wikilink tool in `utils/` + post-move hook in restructure workflow.

### 2.3 Taxonomy ↔ Filesystem Validator
- **Status**: [x] Done (2026-03-24) — Built `validate_taxonomy.py`. Detected 2 untracked folders on first run.
- **Effort**: Small
- **Description**: Script that diffs `taxonomy.md` subcategory definitions against actual `10_Garden/` folder structure. Catches drift immediately (e.g., folder exists but not in taxonomy, or taxonomy defines a category with no folder).

### 2.4 Standardize Scripts to Use `config.py`
- **Status**: [x] Done (2026-03-24) — Rewrote `scan_garden.py`, `check_category_sizes.py`, `audit_frontmatter.py`, `cleanup_empty_dirs.py` to use config paths and thresholds.
- **Effort**: Medium
- **Description**: Many scripts hardcode `r"f:\My Brain\10_Garden"` instead of importing from config. Refactor all preserved scripts to use centralized paths.

---

## Phase 3: Sync Documentation _(reduce confusion)_

### 3.1 Update `task_ingest.md` References
- **Status**: [x] Done (2026-03-24)
- **Effort**: Small
- **Description**: `task_ingest.md` Step 1 references `extract_pdf.py` which is deleted (superseded by `process_inbox.py`). Update all script references in task files to match surviving scripts. Update path references for task files that moved to `tasks/` subfolder.

### 3.2 Update `system_instructions.md` and `README.md`
- **Status**: [x] Done (2026-03-24)
- **Effort**: Small
- **Description**: Update workflow reference paths to point to `tasks/` subfolder. Update README directory structure to reflect current state (AI_Tech merged into Investment/Industry_Analysis, new subcategories, accurate note counts).

---

## Phase 4: Thinking Partner — `brief` Workflow
- **Status**: [x] Done (2026-03-24) — Built `tasks/brief.md` + `workflows/brief.md`
- **Effort**: Medium
- **Impact**: Highest immediate value — makes existing knowledge *usable on demand*
- **Trigger**: `@Agent brief [topic or question]`
- **Description**: Given a topic or question (e.g., "What's my current view on NVIDIA's moat?" or "Prepare me for a semiconductor client meeting"):
  - Pull all relevant notes across categories via keyword + tag matching
  - Synthesize a **briefing document** from accumulated knowledge
  - Highlight where knowledge is fresh vs. potentially stale (using `updated` dates)
  - Flag internal contradictions between notes
  - Add "open questions" not yet answered in the Garden

---

## Phase 5: Thinking Partner — `gaps` Workflow
- **Status**: [x] Done (2026-03-24) — Built `tasks/gaps.md` + `workflows/gaps.md`
- **Effort**: Medium
- **Impact**: Guides future learning and research priorities
- **Trigger**: `@Agent gaps` or `@Agent gaps --category Investment/Industry_Analysis`
- **Description**: Analyze note distribution, recency, and depth across taxonomy:
  - Identify **knowledge blind spots** (few notes, outdated clusters, missing counter-arguments)
  - Cross-reference with professional context (consulting + investing) to prioritize
  - Output a **learning agenda**: "Based on your 16 Memory_Storage notes but 0 on CXL protocol specifics, and given CXL's role in your AI infrastructure thesis, consider..."

---

## Phase 6: Thinking Partner — `challenge` Workflow
- **Status**: [x] Done (2026-03-24) — Built `tasks/challenge.md` + `workflows/challenge.md`
- **Effort**: Medium
- **Impact**: Sharpens investment thesis quality
- **Trigger**: `@Agent challenge [[Note Title]]`
- **Description**: Given a note (investment thesis, industry analysis):
  - Identify **core assumptions** embedded in the note
  - Search Garden for **contradicting evidence** from other notes
  - Apply **pre-mortem thinking**: "It's 12 months later and this thesis failed. What happened?"
  - Output structured challenge: bear case, blind spots, "what would change your mind"

---

## Phase 7: Thinking Partner — `connect` Workflow
- **Status**: [x] Done (2026-03-24) — Built `tasks/connect.md` + `workflows/connect.md`
- **Effort**: Medium
- **Impact**: Deepest long-term value — cross-domain insight generation
- **Trigger**: `@Agent connect [[Note A]] [[Note B]]` or `@Agent connect --discover [[Note A]]`
- **Description**: Given one or two notes:
  - Extract key concepts and structural patterns
  - Scan entire Garden for **non-obvious connections** across categories
  - Generate "bridge insight" that only exists at the intersection
  - Suggest WikiLinks to add
  - Example: Connecting `KV_Cache記憶體架構革命` with `投資槓桿策略` → "Both optimize scarce resources through tiered allocation"

---

---

## Future Improvements (Planned)
- [ ] Obsidian Dataview queries for dashboards
- [ ] Voice memo transcription pipeline
- [ ] Garden note staleness alerts in weekly review
- [ ] Auto-promotion suggestions based on Lab maturity signals
