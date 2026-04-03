# Task: Promote Project Insight to Garden
# Trigger: When user says "promote [[Note]]", "promote [path]", or "promote --scan [project folder]"

> **Guiding Principles**: Apply `.agent/user_persona.md` — the Garden is for durable, cross-context knowledge. Project notes are ephemeral; only insights that transcend a single engagement deserve Garden residency. This is how consulting experience compounds.

## Purpose

Move durable insights from project notes into the Garden knowledge base. Strip client-specific context, reformat into Garden note template, route to the correct category, and maintain bidirectional links between the project origin and the new Garden note.

## Input

The user provides either:
- A specific project note: `promote 20_Projects/Consulting/ClientA/Research/semiconductor_analysis.md`
- A scan directive: `promote --scan 20_Projects/Consulting/ClientA/`

## Process

### Step 1: Read the Source Material

1. If a specific note is provided, read it fully.
2. If `--scan` is used, scan all notes in the project folder (Research/, Meetings/, Decisions/) and list candidates with a one-line summary of each.

### Step 2: Evaluate Durability

Apply the promotion test: **"Would this be useful for a different client or a future investment decision?"**

Criteria for promotion:
- **Industry insight**: generalizable trend, market dynamic, or technology shift
- **Framework or methodology**: a reusable analytical approach developed during the project
- **Counter-intuitive finding**: something that challenged prior assumptions
- **Data point with shelf life**: a benchmark, metric, or reference point useful beyond this project

Criteria for rejection:
- Client-specific operational detail
- Meeting logistics or project management artifacts
- Analysis that only makes sense in the context of one client's situation

If `--scan`, present the evaluation to the user and let them select which notes to promote.

### Step 3: Promote

For each note being promoted:

1. **Extract durable insight**: Distill the generalizable knowledge, stripping client names, project-specific framing, and confidential details.

2. **Reformat into Garden note template**:

```markdown
---
title: [Descriptive Title]
created: [original note date]
updated: [today]
review_by: [today + 6 months]
tags: [relevant tags from taxonomy]
source_type: project_insight
source_project: [[Project Brief Title]]
---

# [Title]

## 摘要
[2-3 sentence summary of the insight]

## 核心發現
[The main finding or conclusion, fully developed]

## 相關概念連結
- [[Existing Garden Note 1]] — [how it relates]
- [[Existing Garden Note 2]] — [how it relates]

## 關鍵洞察
[Deeper implications — what does this mean for the broader industry/theme?]

## 第二層思考
[Second-level thinking: what do most people miss about this? What are the non-obvious consequences?]

## 第一性原理分析
[First principles: strip away assumptions and rebuild the logic from fundamentals]
```

3. **Route to correct Garden category**: Use `.agent/taxonomy.md` keyword matching to determine the appropriate category and subcategory folder.

4. **Add WikiLinks**:
   - In the new Garden note: link back to the originating project brief
   - In the new Garden note: link to existing related Garden notes
   - In the original project note: add `promoted_to: [[Garden Note Title]]` to frontmatter

### Step 4: Update Indices

Run `python .agent/generate_indices.py [CategoryName]` for the affected Garden category to regenerate both Tier 1 and Tier 2 indices.

### Step 5: Output

Provide confirmation:

```
✅ Promoted: [original note] → [[New Garden Note Title]]
   Category: [Garden category/subcategory]
   Path: [full path to new Garden note]
   Links added: [N] WikiLinks to existing Garden notes
   Index updated: [category] topic index regenerated
```

## Quality Checklist

- [ ] Insight is genuinely durable — useful beyond the original context
- [ ] Note follows Garden template exactly (all sections populated)
- [ ] Routed to correct category per taxonomy.md
- [ ] WikiLinks to existing related Garden notes are meaningful, not just tag matches
- [ ] `python .agent/generate_indices.py [Category]` has been run for affected category
- [ ] Language: Traditional Chinese section headers, English technical terms
