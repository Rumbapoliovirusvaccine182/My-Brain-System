# Task: Promote Lab Entry to Garden
# Trigger: When user says "promote" on a 30_Lab/ note, or "lab review"

> Extends the existing `promote.md` workflow for Lab-originated content.

## Purpose

Graduate a Lab entry (thesis, essay, or sparring conclusion) into a Garden note. Applies the same durability test and redaction rules as project promotion, but with Lab-specific handling.

## Process

### Step 1: Evaluate Readiness

Check the Lab entry's `status` field:
- `wip` → Not ready. Tell the user what's missing (open questions, weak evidence, untested angles). Suggest a `spar` session if the thesis needs stress-testing.
- `review` → Ready for promotion evaluation. Proceed.

### Step 2: Apply Durability Test

Same as `promote.md`: **"Would this be useful in a different context, six months from now?"**

For sparring artifacts specifically: promote the **conclusion**, not the conversation. The conversation stays in Lab as the audit trail.

### Step 3: Promote

1. Extract the durable insight from the Lab entry.
2. Create Garden note using standard Garden template (see `promote.md` Step 3).
3. Route to correct category via `taxonomy.md`.
4. Add WikiLinks bidirectionally:
   - Garden note → Lab origin (`source_type: lab_insight`, `source_lab: [[Lab Note]]`)
   - Lab note → Garden note (add `promoted_to: [[Garden Note]]` to frontmatter)
5. Update Lab entry status to `promoted`.

### Step 4: Archive Stale Lab Entries

When running `lab review`, also flag Lab entries older than 90 days still in `wip`:
- Present to user with options: promote, spar again, or archive.
- Archived entries move to `99_Archives/Lab/` with status set to `archived`.

## Quality Checklist

- [ ] Only `review`-status entries promoted (or user explicitly overrides)
- [ ] Conclusion promoted, not raw conversation
- [ ] Standard Garden template and redaction rules applied
- [ ] Bidirectional links between Lab origin and Garden note
- [ ] Stale WIP entries flagged (if running `lab review`)
