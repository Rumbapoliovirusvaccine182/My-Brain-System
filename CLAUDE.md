# My Brain — Obsidian Knowledge System

## What This Is
An AI-powered Obsidian knowledge management system that turns scattered information into an interconnected, searchable knowledge graph. Built for anyone who needs to synthesize research across multiple domains.

Core capabilities:
1. **Knowledge Garden** (`10_Garden/`) — permanent notes with auto-categorization and WikiLink generation
2. **Thinking Lab** (`30_Lab/`) — WIP theses, essays, and explorations with AI co-creation & sparring
3. **Self-Evolving Taxonomy** — folder structure reorganizes itself based on MECE + Pyramid principles

## Directory Structure
```
00_Inbox/          → Raw files awaiting ingestion
10_Garden/         → Permanent notes (max 3 levels, MECE + Pyramid structure)
  AI_Hardware/     → Compute, Memory, Networking/Optics, Packaging/Mfg, Infra/Power, Testing
  AI_Software/     → Applications, Software_Trends, Products
  Industry_Verticals/ → Automotive, Clean_Energy, Space, Robotics, Commodities
  Investment_Thinking/ → Investor_Mindset, Market_Behavior, Frameworks, Trading, Valuation
  Macro_Markets/   → Geopolitics, Portfolio_Reviews
  Journal/         → Personal reflections, essays
  Parenting/       → Education, family
30_Lab/            → Active thinking workspace (WIP — promote or archive)
  Theses/          → Developing investment/industry theses
  Essays/          → Long-form writing drafts
  Scratch/         → Quick explorations, what-ifs, throwaway analysis
99_Archives/
  Assets/          → Original source PDFs/images
  Lab/             → Archived Lab entries (dead-ended or superseded)
.agent/            → System config, scripts, workflows, tasks
```

## Key References
| File | Purpose |
|------|---------|
| `.agent/taxonomy.md` | Category definitions, keywords, subcategory routing |
| `.agent/user_persona.md` | Analysis quality framework (So What test, first principles, success metrics) |
| `.agent/writing_style.md` | User's writing voice and platform preferences — consult when polishing |
| `.agent/BACKLOG.md` | System roadmap and completion log |

## Critical Rules

### Language & Format
- **All Garden notes**: Traditional Chinese (繁體中文). Technical terms stay English (GPU, M&A, PMI, CoWoS, etc.)
- **Strictly Markdown** (.md) with YAML frontmatter
- **Tone**: Professional, concise, strategic framing. Cut the fluff. Occasional humor OK.

### Knowledge Integrity
- **Never delete information** — refactor and preserve meaning
- **WikiLinks are mandatory** — `[[Note Title]]` connections between concepts. Orphaned notes are incomplete.
- **Garden vs Lab**: Garden = permanent knowledge. Lab = active thinking (WIP). Bridge via `promote` workflow.
- **Lab lifecycle**: Everything in Lab is WIP. Entries must eventually be promoted to Garden or archived. No permanent residents.
- **AI sessions are co-located**: Sparring and co-creation logs live inside the Lab entry itself (`## 工作紀錄`), not in a separate folder. The thinking stays with the artifact.

### Analysis Mindset
- **"So What?" test**: Every note, every insight must answer "Why does this matter?" Lead to actionable conclusions.
- **Cross-industry lens**: Always consider how knowledge from one domain applies to others. Look for transferable patterns.
- **Second-order thinking**: Don't just summarize. What are others NOT seeing? What are the second-order consequences?
- **Knowledge as Graph**: This system is a knowledge graph, not an archive. Cross-category WikiLinks are a success metric.

## Knowledge Gap Tracking (`.agent/gaps/`)
- Gap reports are persistent artifacts saved as `YYYY-MM-DD_[scope].md`
- Each gap has a unique ID, fill criteria, and filled counter
- Ingest workflow auto-checks new notes against active gap reports
- Reports stay `active` until superseded by a fresh scan of the same scope

## Workflow Quick Reference

### Data Management
| Trigger | Task file |
|---------|-----------|
| `@Agent run ingest` | `tasks/ingest.md` — Process Inbox → Garden notes |
| `@Agent sort-garden` | `tasks/restructure.md` — Reorganize/re-categorize Garden |
| `@Agent process-files` | `tasks/process_files.md` — Convert Office files → markdown |

### Thinking Partner
| Trigger | Task file |
|---------|-----------|
| `@Agent recall [topic]` | `tasks/recall.md` — Quick pull, no synthesis |
| `@Agent brief [topic]` | `tasks/brief.md` — Synthesize knowledge briefing |
| `@Agent gaps` | `tasks/gaps.md` — Knowledge gap analysis + learning agenda |
| `@Agent challenge [[Note]]` | `tasks/challenge.md` — Stress-test thesis |
| `@Agent connect [[A]] [[B]]` | `tasks/connect.md` — Cross-domain insight discovery |

### Thinking Lab
| Trigger | Task file |
|---------|-----------|
| `@Agent session [topic]` | `tasks/session.md` — Co-create + spar fluidly |
| `@Agent spar [topic]` | `tasks/spar.md` — Session in adversarial mode |
| `@Agent learn-style` | `tasks/learn_writing_style.md` — Analyze Lab writing → update style guide |
| `@Agent draft-post [[Note]]` | `tasks/draft_post.md` — Turn note into social media draft |
| `@Agent lab-promote` | `tasks/lab_promote.md` — Promote Lab entry → Garden |
| `@Agent lab-review` | `tasks/garden_review.md` — Review Lab entries |
| `@Agent garden-review` | `tasks/garden_review.md` — Surface stale Garden notes |

### Knowledge Promotion
| Trigger | Task file |
|---------|-----------|
| `@Agent promote` | `tasks/promote.md` — Move durable insights → Garden |
| `@Agent memo` | `tasks/memo.md` — Structure investment memo |

## Garden Structural Principles (enforced by sort-garden)
- **MECE**: Sibling folders don't overlap. Each note has exactly one correct home.
- **Pyramid**: Max 3 levels. 3-8 children per parent. Balanced sizing (5:1 max ratio).
- **Leaf sizing**: 5-20 notes ideal. >20 = consider split. >30 = strongly split. <3 = merge.
- **No phantom parents**: Folders that exist only as routing layers get eliminated.
- **Top-level = mental model**: 5-8 categories reflecting how you think about knowledge.

## Two-Tier Index System
- **Tier 1 (Parent)**: Lightweight routing index (<3KB) — subcategory list with descriptions, note counts. Helps agents decide which subfolder to drill into.
- **Tier 2 (Leaf)**: Compact table index (3-8KB) — one row per note with title, key thesis (<20 words), key entities. For detailed lookup.
- **Script**: `python .agent/generate_indices.py` regenerates all indices. Accepts optional category scope: `python .agent/generate_indices.py AI_Hardware`
- **Rule**: Index name MUST match folder name. Delete stale indices before regenerating.

## Commit Convention
```
<type>: <brief description>
```
Types: `feat`, `fix`, `refactor`, `docs`, `chore`
