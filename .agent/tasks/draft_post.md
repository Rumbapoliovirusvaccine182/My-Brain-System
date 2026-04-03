# Task: Draft Social Media Post
# Trigger: When user says "draft-post [Lab note]", "thread [[Note]]", or "post [[Note]]"

> **Style Reference**: Always consult `.agent/writing_style.md` before drafting or polishing. Match the user's voice, not a generic "content creator" tone.

## Purpose

Convert Lab entries (or Garden notes) into social media drafts — Twitter/X threads, LinkedIn posts, or other formats. Output goes to `30_Lab/Essays/` as a draft for user review before publishing.

## Input

The user provides:
- A Lab or Garden note: `draft-post [[My HBM Thesis]]`
- Optional platform: `draft-post [[Note]] --twitter` or `--linkedin`
- Optional: `polish` (user has already written a draft, wants editing only)

## Process

### Step 1: Read Source + Style Guide

1. Read the referenced note fully.
2. Read `.agent/writing_style.md` for voice, tone, and platform preferences.
3. Identify the single strongest insight — social posts need one clear takeaway, not a survey.

### Step 2: Draft

**For Twitter/X threads:**
1. Hook tweet: the most surprising or contrarian claim. No throat-clearing.
2. Body tweets (3-8): build the argument. One idea per tweet. Data points earn their place.
3. Closing tweet: so-what or call to action.
4. Each tweet ≤ 280 chars. Mark thread breaks clearly.

**For LinkedIn:**
1. Opening line: hook that survives the "see more" fold.
2. Body: structured argument, slightly more formal than Twitter.
3. Closing: insight or question that invites engagement.

**For polish requests:**
1. Read the user's draft.
2. Edit for voice consistency (per style guide), clarity, and punch.
3. Show changes as tracked edits (old → new) so user can accept/reject.

### Step 3: Output

1. Save draft to `30_Lab/Essays/YYYY-MM-DD_post_[topic-slug].md`
2. Frontmatter: `type: post`, `platform: [twitter|linkedin|etc]`, `source: [[Original Note]]`, `status: draft`
3. Present the draft inline for immediate user feedback.

### Step 4: Iterate

User reviews and says what to change. Repeat until they're happy. Update the draft file each round.

## Quality Checklist

- [ ] `.agent/writing_style.md` consulted before drafting
- [ ] Single clear takeaway identified — not trying to say everything
- [ ] Platform constraints respected (char limits, tone)
- [ ] User's voice, not generic AI copywriting
- [ ] Draft saved to Lab with correct frontmatter
- [ ] WikiLink back to source note
