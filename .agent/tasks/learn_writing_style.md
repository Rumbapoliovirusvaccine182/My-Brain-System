# Task: Learn Writing Style from Samples
# Trigger: When user says "learn my style", "analyze my writing", or "learn-style"

> **Output**: Updates `.agent/writing_style.md` with patterns extracted from user's actual writing.

## Purpose

Analyze the user's writing in `30_Lab/` (Theses, Essays, Scratch) and extract recurring patterns into the writing style guide. The Lab is where the user writes — theses, essays, explorations — making it the most authentic source of their voice. This is cumulative — each run refines the style profile, not replaces it.

## Input

Two modes:

**Full scan** (`@Agent learn-style`): Scan `30_Lab/` recursively (all subfolders: `Theses/`, `Essays/`, `Scratch/`). Read all `.md` files as writing samples. Additionally, if `.agent/Writing_Samples/` exists and contains files, include those too (legacy support).

**Targeted** (`@Agent learn-style [[Note]]` or `@Agent learn-style "path/to/file"`): Analyze only the specified file. Faster, avoids re-reading already-learned material. Use this when the user has just written or updated a specific document.

Accepted formats:
- `.md` files (theses, essays, explorations, posts)
- `.txt` files
- Screenshots (read and extract text)
- `.pdf` files
- Office files (run `process_files` first if needed)

## Process

### Step 1: Read All Samples

1. Scan `30_Lab/` recursively for all `.md` files (Theses/, Essays/, Scratch/).
2. If `.agent/Writing_Samples/` exists, also scan it (legacy drop folder).
3. Read each sample fully.
4. Note the type/context: thesis draft, essay, scratch exploration, social media post, etc.

### Step 2: Extract Patterns

Analyze across ALL samples (not just one) for:

**Voice & Tone**
- Formality level (casual ↔ academic)
- Use of humor, irony, or provocation
- First person vs. third person vs. impersonal
- Confidence level (hedging vs. assertive)
- EN/ZH code-switching patterns

**Structure**
- How arguments open (question? claim? anecdote? data?)
- Paragraph/tweet rhythm (short-long-short? building crescendo?)
- How arguments close (so-what? call to action? open question?)
- Use of lists, numbering, headers

**Language**
- Sentence length distribution (punchy short? complex compound?)
- Favorite words, phrases, or constructions that recur
- Technical term handling (defined inline? assumed knowledge?)
- Metaphor/analogy patterns

**Platform-Specific**
- Thread structure (hook style, tweet count, transitions)
- LinkedIn tone vs. Twitter tone
- Hashtag and emoji usage (or lack thereof)

**Anti-Patterns**
- What the user consistently does NOT do (important negative signal)

### Step 3: Update Style Guide

1. Read current `.agent/writing_style.md`.
2. Merge new findings with existing entries (don't overwrite confirmed patterns).
3. Add concrete examples from the samples — quote actual phrases as reference.
4. Update the revision log with date and what was learned.

### Step 4: Archive Samples

- Lab files (`30_Lab/`): Do NOT move — they stay in place as living documents.
- Legacy drop folder files (`.agent/Writing_Samples/`): Move to `99_Archives/Assets/Writing_Samples/` after processing.

### Step 5: Report

Present findings to user:
- "Here's what I learned from these N samples"
- Key patterns identified (with examples)
- Any contradictions or ambiguities to clarify
- Ask if anything should be corrected

## Quality Checklist

- [ ] All samples in folder processed
- [ ] Patterns extracted across samples, not from a single one
- [ ] `.agent/writing_style.md` updated with concrete examples
- [ ] Revision log entry added
- [ ] Samples archived out of drop folder
- [ ] Findings presented to user for confirmation
