# Task: Working Session
# Trigger: "session [topic]", "session [[Lab Note]]", "spar [topic]", "let's work on [topic]", "let's think through [topic]"

> **Guiding Principles**: Apply `.agent/user_persona.md`. In co-create mode, build constructively. In spar mode, push back hard — steelman first, then attack the weakest point. In practice, shift fluidly between both stances based on what the content needs.

## Purpose

Run an AI working session on a topic, developing thesis, or draft. Sessions alternate between co-creation (building together) and sparring (stress-testing). The session log is saved inside the Lab entry itself, keeping the thinking co-located with the artifact.

## Input

The user provides either:
- A topic: `session "Is HBM overbuilt for inference workloads?"`
- An existing Lab note: `session [[My HBM Thesis]]`
- A Garden note to challenge: `spar [[Garden Note Title]]`
- A stance hint: `spar` starts adversarial, `session` starts collaborative — but both can shift

## Process

### Step 1: Set Up

1. If an existing note is referenced, read it fully to understand the current state.
2. If a raw topic, check Garden for relevant notes. Ask the user for their initial take if unclear.
3. If no Lab entry exists yet, create one from `_Templates/Lab_Entry.md` in the appropriate Lab subfolder:
   - Investment/industry angle → `30_Lab/Theses/`
   - Long-form writing → `30_Lab/Essays/`
   - Quick exploration → `30_Lab/Scratch/`
   - Filename: `YYYY-MM-DD_[short-topic-slug].md`

### Step 2: Work

Run iterative rounds. Each round uses the stance the content needs:

**Co-create stance** (building):
1. Extend, refine, or restructure the user's thinking.
2. Pull in relevant Garden knowledge or frameworks.
3. **Web search** to fill gaps the Garden can't answer — recent earnings, industry data, news, analyst reports. Prioritize: company IR pages, industry conferences, sell-side previews, trade publications.
4. Draft sections, sharpen arguments, fill gaps together.

**Spar stance** (challenging):
1. **Steelman**: Restate the user's position in its strongest form.
2. **Challenge**: Attack the weakest point — use data from Garden, logical gaps, or counter-frameworks.
3. **Invite response**: Ask the user to defend, concede, or pivot.

Shift stance fluidly based on signals:
- User is exploring → co-create
- User has a firm position → spar to test it
- Argument has a gap → spar that specific point, then co-create the fix

Continue until:
- The user says "enough" or "land it"
- The position has stabilized (two rounds with no material change)
- A clear fork has emerged (two viable but incompatible conclusions)

### Step 3: Converge

1. Summarize the final state vs. the starting state.
2. Identify what changed and why.
3. Flag open questions that emerged.
4. Append the session log to the Lab entry's `## 工作紀錄` section:
   - Date, mode (co-create / spar / mixed), one-line summary
   - Key rounds with position → evolution

### Step 4: Link and Route

1. Add WikiLinks to relevant Garden notes referenced during the session.
2. Update `related_lab` frontmatter if connected to other Lab entries.
3. Update `## 當前思考` and `## 已知弱點` sections to reflect current state.
4. If the conclusion is mature enough, suggest promotion:
   - To Garden (durable insight)
   - Stay in Lab (needs more development)
   - Archive (dead-ended — record why)

## Quality Checklist

- [ ] Session logged in the Lab entry's `## 工作紀錄` section
- [ ] Entry's `## 當前思考` updated to reflect post-session position
- [ ] WikiLinks to Garden notes and related Lab entries
- [ ] Status set correctly (wip if ongoing, review if ready for promote decision)
- [ ] `updated` frontmatter date refreshed
- [ ] Language: Traditional Chinese section headers, English technical terms
