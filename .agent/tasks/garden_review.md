# Task: Garden Review — Surface Stale Notes
# Trigger: When user says "garden-review", "review garden", or "what's stale?"

> **Guiding Principles**: The Garden is only valuable if it reflects current reality. A note with an expired thesis is worse than no note — it creates false confidence.

## Purpose

Systematically surface Garden notes that are past their `review_by` date or show signs of decay, then guide the user through a keep/update/archive decision for each.

## Process

### Step 1: Scan for Review Candidates

Scan all `10_Garden/` notes and flag candidates in three tiers:

**Tier 1 — Overdue** (highest priority)
- `review_by` date has passed
- Sort by how far overdue (worst first)

**Tier 2 — Potentially Stale** (heuristic)
- `updated` date > 6 months ago AND no `review_by` set
- Notes referencing specific data points, forecasts, or market conditions (these decay fastest)
- Notes with tags related to fast-moving domains: AI hardware roadmaps, market pricing, policy/regulation

**Tier 3 — Orphaned**
- Notes with zero incoming WikiLinks (nothing references them)
- Notes that only link to other notes that have been archived or deleted

### Step 2: Present Review Queue

For each candidate, show:
```
📋 [Note Title]
   Category: [path]
   Last updated: [date] ([N months ago])
   Review by: [date] ([N days/months overdue]) or "not set"
   Risk: [what specifically might be stale — e.g., "references NVIDIA roadmap from 2024"]
   Links: [N] incoming, [N] outgoing
```

Group by category. Show count summary first:
```
Garden Review: [N] overdue, [N] potentially stale, [N] orphaned
```

### Step 3: User Decision per Note

For each note, user chooses:

| Action | What happens |
|--------|-------------|
| **keep** | Bump `review_by` forward 6 months, update `updated` date |
| **update** | Open for editing — user or agent updates the content, reset `review_by` |
| **spar** | Thesis needs stress-testing → launch `spar` session on this note |
| **merge** | Content overlaps with another note → merge and redirect WikiLinks |
| **archive** | Thesis is dead or superseded → move to `99_Archives/Garden/` with `status: archived` |
| **skip** | Leave for next review cycle |

### Step 4: Batch Processing

Allow the user to process in batch:
- `keep all` for a category (if they've mentally reviewed)
- `skip tier 3` to focus on overdue first
- Process one-by-one for Tier 1

### Step 5: Summary Report

After processing, show:
```
Garden Review Complete
  Reviewed: [N] notes
  Kept (refreshed): [N]
  Updated: [N]
  Sent to spar: [N]
  Merged: [N]
  Archived: [N]
  Skipped: [N]

  Next review candidates: [date of earliest upcoming review_by]
```

### Step 6: Set Missing review_by

For any Garden note touched during this review that lacks a `review_by` field, add one:
- Fast-decay topics (AI hardware, market data, policy): `today + 3 months`
- Medium-decay (industry trends, frameworks): `today + 6 months`
- Slow-decay (first principles, mental models): `today + 12 months`

## Scheduled Cadence

Suggest running `garden-review` monthly. The `weekly-review` workflow should include a one-line flag if any Garden notes are overdue:
```
⚠️ [N] Garden notes past review date — run `garden-review` to triage
```

## Quality Checklist

- [ ] All three tiers scanned (overdue, stale, orphaned)
- [ ] Candidates presented with enough context to decide without re-reading
- [ ] User decision recorded for each note
- [ ] `review_by` and `updated` fields updated for kept/updated notes
- [ ] Archived notes moved to `99_Archives/Garden/`
- [ ] Merged notes have WikiLinks redirected
- [ ] Summary report generated
- [ ] Missing `review_by` fields backfilled with decay-appropriate dates
