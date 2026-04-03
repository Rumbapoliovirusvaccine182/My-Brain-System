# Task: Recall — Quick Knowledge Pull
# Trigger: When user says "recall [topic]", "what do I know about [topic]", or "pull [topic]"

> **Design intent**: Fast retrieval, not synthesis. The user wants to see what's in the system, not a briefing. Save analysis for `brief`.

## Purpose

Quickly surface all relevant Garden + Lab notes on a topic with one-line summaries. No synthesis, no commentary — just a clean inventory of what the system holds.

## Input

A topic, keyword, or theme: `recall HBM`, `recall packaging`, `recall tariff risk`

## Process

### Step 1: Search

Search across both `10_Garden/` and `30_Lab/` using:
1. **Title match**: topic appears in filename
2. **Tag match**: topic appears in frontmatter `tags`
3. **Content match**: topic appears in note body (keyword + related terms)
4. **WikiLink match**: notes that link to notes matching the topic

Use `.agent/taxonomy.md` to expand the search with related keywords (e.g., "HBM" should also match "High Bandwidth Memory", "memory", "SK Hynix", "Samsung memory").

### Step 2: Present Results

Group by location and relevance:

```
🔍 Recall: [topic]

── Garden ([N] notes) ──────────────────
■ [[Note Title]] — [one-line summary from 摘要 section]
  [category path] · updated [date] · [N] links
■ [[Note Title]] — [one-line summary]
  [category path] · updated [date] · [N] links

── Lab ([N] entries) ───────────────────
◆ [[Note Title]] — [one-line summary] [WIP|review]
  [lab subcategory] · updated [date]

── Mentions ([N] notes) ────────────────
○ [[Note Title]] — [topic] referenced in context of [brief context]
```

**Relevance tiers**:
- `■` / `◆` = primary match (title, tags, or major subject)
- `○` = mention (topic appears but isn't the main subject)

### Step 3: Quick Stats

```
Total: [N] Garden + [N] Lab + [N] mentions
Coverage: [brief assessment — e.g., "deep on supply side, thin on demand forecasts"]
Freshest: [[Note]] ([date])
Stalest: [[Note]] ([date]) ⚠️ if > 6 months
```

### Step 4: Suggest Next Action (one line only)

Based on what was found, suggest ONE of:
- `brief [topic]` — if there's enough material for synthesis
- `spar [topic]` — if there's a developing thesis worth testing
- `gaps [topic]` — if coverage looks thin
- Nothing — if the user just needed the inventory

## What This Is NOT

- Not `brief` — no synthesis, no narrative, no recommendations
- Not `gaps` — doesn't analyze what's missing (though it hints at coverage)
- Not `connect` — doesn't find cross-domain bridges

This is a lookup. Fast in, fast out.

## Quality Checklist

- [ ] Both Garden and Lab searched
- [ ] Taxonomy keyword expansion applied
- [ ] Results grouped by location and relevance tier
- [ ] One-line summaries are actually one line (not paragraphs)
- [ ] Quick stats include freshness assessment
- [ ] Single next-action suggestion (or none)
- [ ] Completed in under 30 seconds of processing
