# Task: Knowledge Gaps & Learning Radar
# Trigger: When user says "gaps", "learning radar", "what should I study", or "gaps --category [path]"

> **Guiding Principles**: Apply `.agent/user_persona.md` — especially the dual-purpose lens. Gaps should be evaluated through both consulting and investment value.

## Purpose

Analyze the knowledge base's coverage and identify blind spots, outdated clusters, and missing perspectives. Output a prioritized learning agenda that tells the user not just what's missing, but **why it matters** given their professional context.

## Process

### Step 1: Inventory the Garden

1. Walk the entire `10_Garden/` directory tree.
2. For each leaf folder (no subdirectories), count notes and record:
   - Note count
   - Average `updated` date (freshness)
   - Number of notes past `review_by` date
   - Tag distribution
3. If `--category [path]` is specified, narrow scope to that subtree only.

### Step 2: Quantitative Gap Analysis

Produce metrics for each category/subcategory:

| Metric | Calculation |
|--------|------------|
| **Coverage depth** | Note count per subcategory |
| **Freshness score** | % of notes updated in last 3 months |
| **Staleness risk** | % of notes past review_by date |
| **Connectivity** | Average WikiLinks per note |
| **Perspective balance** | Are there both bull AND bear views? (for investment topics) |

### Step 3: Identify Gap Types

**Type 1 — Empty Zones**: Taxonomy subcategories with < 3 notes. These are declared interest areas with no substance.

**Type 2 — Stale Clusters**: Subcategories where > 50% of notes are past review_by. Knowledge is decaying.

**Type 3 — One-Sided Views**: Investment subcategories with no contrarian or risk analysis. (Check: does the folder have notes with bear case, risk, or contrarian tags?)

**Type 4 — Missing Adjacencies**: Cross-domain connections that *should* exist based on the taxonomy but don't. For example:
- If you have 16 Memory_Storage notes but 0 mention CXL protocol → CXL is an adjacency gap
- If you have AI_Infra notes about power but none linking to Clean_Energy → missing cross-domain link

**Type 5 — Professional Blind Spots**: Areas critical to user's consulting + investing profile (per user_persona.md) that have no coverage:
- PMI (Post-Merger Integration) frameworks → consulting core skill
- SaaS metrics / unit economics → common due diligence area
- Regulatory/compliance trends → affects multiple industries

### Step 4: Prioritize and Output

Produce the learning agenda in Traditional Chinese:

```markdown
# 知識缺口分析 (Knowledge Gaps Report)

> 掃描日期: [today] | 涵蓋範圍: [全庫 or specific category]

## 📊 覆蓋概況

| 類別 | 筆記數 | 新鮮度 | 連結密度 | 狀態 |
|------|--------|--------|----------|------|
| ... | ... | ...% | avg N | 🟢/🟡/🔴 |

## 🔴 高優先缺口 (High Priority Gaps)

### 1. [Gap Name]
- **缺口類型**: [Empty Zone / Stale Cluster / One-Sided / Missing Adjacency / Professional Blind Spot]
- **現狀**: [e.g., "CXL 協議在 16 篇 Memory_Storage 筆記中完全未提及"]
- **為什麼重要**: [Frame in terms of consulting value AND investment relevance]
- **建議行動**: [Specific — name a report type, company, or concept to research]
- **預期影響**: [What connecting this gap would unlock in your thinking]

### 2. [Gap Name]
...

## 🟡 中優先缺口 (Medium Priority)
[Same structure, shorter descriptions]

## 🟢 覆蓋良好 (Well-Covered Areas)
[Brief acknowledgment of strengths — which areas are deep and fresh]

## 🔄 需要更新的筆記 (Notes Needing Refresh)
[List of specific notes past review_by date, grouped by urgency]

## 📋 30 天學習計劃 (30-Day Learning Agenda)
[Concrete, prioritized list of 5-7 specific research actions]
1. **Week 1**: ...
2. **Week 2**: ...
3. **Week 3-4**: ...
```

### Step 5: Save Gap Report as Persistent Artifact

After presenting the report to the user, save a structured version to `.agent/gaps/`:

1. **Filename**: `YYYY-MM-DD_[scope].md` (e.g., `2026-03-29_AI_Hardware.md`)
2. **Format**: Each gap gets a unique ID (GAP-1, GAP-2, ...) with:
   - Type, description of what's missing
   - **Fill criteria**: concrete, measurable conditions for closing the gap (e.g., "≥3 notes covering X" or "≥5 WikiLinks between X and Y")
   - **Filled counter**: starts at 0, updated by ingest workflow
3. **Frontmatter**: `scope`, `generated`, `status: active`, `total_notes_at_scan`
4. **Lifecycle**: Reports stay `active` until a new gaps scan for the same scope supersedes them, at which point the old one becomes `status: superseded`.

This creates a persistent record that the ingest workflow checks against (see ingest.md Step 5).

## Quality Checklist

- [ ] Gaps are ranked by professional relevance, not just note count
- [ ] Each gap explains WHY it matters (not just "you have few notes here")
- [ ] Learning agenda is concrete (names specific topics, not vague areas)
- [ ] Well-covered areas acknowledged (avoids being purely negative)
- [ ] Cross-domain gaps identified (not just within-category)
- [ ] Gap report saved to `.agent/gaps/` with fill criteria
- [ ] Language: Traditional Chinese with English technical terms
