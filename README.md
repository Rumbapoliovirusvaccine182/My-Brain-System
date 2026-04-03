# 🧠 My Brain System

**An AI-powered knowledge management system built on Obsidian and Claude Code.**

Turn scattered research, articles, and ideas into an interconnected knowledge graph that evolves with you. Drop files in, get structured insights out.

---

## The Problem

You read 50 articles a week. You bookmark them. You forget them. Six months later, you can't find the one insight that would connect two ideas you're working on.

Most note-taking systems are filing cabinets — they store information but don't *think* with you.

## The Solution

This system does three things traditional note apps can't:

1. **Ingests and analyzes** — Drop a PDF, screenshot, or article into the inbox. The AI reads it, extracts insights, generates WikiLinks to your existing knowledge, and files it into the right category.

2. **Self-organizes** — Run `sort-garden` and the folder structure reorganizes itself using MECE + Pyramid principles. Categories split, merge, and rebalance as your knowledge grows. No manual filing.

3. **Thinks with you** — Co-create investment theses, stress-test arguments with adversarial sparring, discover cross-domain connections you'd never see manually.

---

## Architecture

```
📱 LINE / Mobile                    🖥️ Obsidian + Claude Code
     │                                      │
     │  Send article URL,                   │  @Agent run ingest
     │  forward PDF,                        │  @Agent session [topic]
     │  share social post                   │  @Agent sort-garden
     │                                      │  @Agent brief [topic]
     ▼                                      ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│  LINE    │───▶│  Make.com    │───▶│  00_Inbox/   │
│  Chat    │    │  Automation  │    │  (raw files) │
└──────────┘    └──────────────┘    └──────────────┘
                       │                    │
                 Routes by type:      AI Agent processes:
                 • PDF → Drive → Inbox     • Extract & analyze
                 • URL → Gemini → .md      • Categorize via taxonomy
                 • Image → Drive → Inbox   • Generate WikiLinks
                                           • File into Garden
                                            │
                                            ▼
                                    ┌──────────────┐
                                    │  10_Garden/   │
                                    │  (knowledge   │
                                    │   graph)      │
                                    └──────────────┘
```

### Mobile Capture → Inbox Pipeline

The fastest path from "I just saw something interesting" to structured knowledge:

**[LINE](https://line.me/) → [Make.com](https://www.make.com/) → Obsidian Inbox**

Send anything to a LINE chat — a PDF attachment, a Substack post, a Facebook article, any URL — and a [Make.com automation scenario](https://us2.make.com/public/shared-scenario/0gPrv1m2iGQ/integration-line) routes it into `00_Inbox/`:

| What you send | What happens |
|---------------|-------------|
| **PDF attachment** | Downloaded via LINE API → uploaded to Google Drive → synced to `00_Inbox/` |
| **Article URL** | Fetched via HTTP → processed by Gemini AI into markdown → saved as `.md` in `00_Inbox/` |
| **Social media post** | URL fetched → content extracted → converted to `.md` in `00_Inbox/` |

Once files land in the Inbox, run `@Agent run ingest` in Claude Code to process them into structured Garden notes.

> **Get the Make scenario**: [Import this blueprint](https://us2.make.com/public/shared-scenario/0gPrv1m2iGQ/integration-line) into your Make.com account. You'll need to connect your own LINE, Google Drive, and Gemini API credentials.

---

## Knowledge Garden (`10_Garden/`)

Notes are organized into a self-evolving taxonomy:

```
10_Garden/
├── AI_Hardware/          ← Compute, Memory, Networking, Packaging, Power, Testing
├── AI_Software/          ← Applications, Software Trends, Products
├── Industry_Verticals/   ← Automotive, Clean Energy, Space, Robotics, Materials
├── Investment_Thinking/  ← Mindset, Market Behavior, Frameworks, Trading, Valuation
├── Macro_Markets/        ← Geopolitics, Portfolio Reviews
├── Journal/              ← Personal reflections
└── Parenting/            ← Education, family
```

**This structure is not fixed.** Run `@Agent sort-garden` and the system:
- Scans all notes for semantic clustering
- Proposes folder restructuring based on MECE/Pyramid principles
- Moves files, updates WikiLinks, regenerates indices
- Rewrites `taxonomy.md` — which becomes the basis for the next cycle

### Two-Tier Index System

Every folder has an auto-generated index optimized for both human browsing and AI agent lookup:

- **Tier 1 (Parent folders)**: Lightweight routing index (<3KB) — "which subfolder should I look in?"
- **Tier 2 (Leaf folders)**: Compact table with one row per note — title, key thesis, key entities

Regenerate with: `python .agent/generate_indices.py`

---

## Thinking Lab (`30_Lab/`)

The Lab is where ideas develop before they become permanent knowledge:

| Command | What it does |
|---------|-------------|
| `@Agent session [topic]` | AI working session — co-create and spar fluidly |
| `@Agent spar [topic]` | Adversarial mode — steelman then attack the weakest point |
| `@Agent learn-style` | Analyze your writing patterns → update style guide |
| `@Agent draft-post [[Note]]` | Turn a note into a social media draft |

Sessions are logged inside the Lab entry itself (`## 工作紀錄`), keeping the thinking co-located with the artifact. When an idea matures, `@Agent lab-promote` moves it to the Garden.

---

## All Workflows

### Data Management
| Command | What it does |
|---------|-------------|
| `@Agent run ingest` | Process Inbox → structured Garden notes with WikiLinks |
| `@Agent sort-garden` | Reorganize folder structure using MECE/Pyramid principles |
| `@Agent process-files` | Convert Office files (.pptx/.docx/.pdf) → markdown |

### Thinking Partner
| Command | What it does |
|---------|-------------|
| `@Agent recall [topic]` | Quick inventory — what do I know about X? |
| `@Agent brief [topic]` | Synthesized briefing from all relevant notes |
| `@Agent gaps` | Knowledge gap analysis + 30-day learning agenda |
| `@Agent challenge [[Note]]` | Stress-test a thesis with pre-mortem analysis |
| `@Agent connect [[A]] [[B]]` | Discover non-obvious cross-domain connections |

### Knowledge Lifecycle
| Command | What it does |
|---------|-------------|
| `@Agent promote` | Move durable insights from Lab → Garden |
| `@Agent garden-review` | Surface stale notes for update or archival |
| `@Agent memo` | Structure an investment memo from Garden research |

---

## Getting Started

### Prerequisites
- [Obsidian](https://obsidian.md/) with these plugins: **Dataview**, **Templater**, **Strange New Worlds**
- [Claude Code](https://claude.ai/claude-code) (CLI or VS Code extension)
- Python 3.10+ (for index generation scripts)
- Optional: [Make.com](https://www.make.com/) account + [LINE](https://line.me/) for mobile capture

### Setup

1. **Clone this repo**
   ```bash
   git clone https://github.com/Timeverse/My-Brain-System.git
   cd My-Brain-System
   ```

2. **Open in Obsidian** — point Obsidian at the cloned folder as a vault

3. **Customize your taxonomy** — edit `.agent/taxonomy.md` to match your knowledge domains. The default categories are investment/tech-focused; replace them with whatever you study.

4. **Drop files into `00_Inbox/`** and run:
   ```
   @Agent run ingest
   ```

5. **Optional: Set up mobile capture** — import the [Make.com scenario](https://us2.make.com/public/shared-scenario/0gPrv1m2iGQ/integration-line) and connect your LINE + Google Drive

---

## Design Principles

- **MECE + Pyramid**: Sibling folders don't overlap. Max 3 levels deep. 5-20 notes per leaf.
- **Knowledge as Graph**: WikiLinks between notes are a first-class success metric. Orphaned notes are incomplete.
- **"So What?" Test**: Every insight must answer why it matters. No summaries without conclusions.
- **Evolution over Perfection**: Each `sort-garden` cycle makes incremental improvements. The structure is never "done."
- **Never Delete**: Refactor and preserve meaning. Archive, don't destroy.

---

## Note Format

Every Garden note follows this structure (Traditional Chinese headers, English technical terms):

```markdown
---
title: [Descriptive Title]
created: 2026-04-03
updated: 2026-04-03
review_by: 2026-10-03
tags: [Category, Subcategory, Keywords]
source_type: pdf_report
source_asset: original_filename.pdf
---

# Title

## 摘要 (Summary)
## 核心發現 (Core Findings)
## 相關概念連結 (Related Concepts)     ← WikiLinks to other notes
## 關鍵洞察 (Key Insights)              ← Must pass "So What?" test
## 第二層思考 (Second-Level Thinking)    ← What are others NOT seeing?
## 第一性原理分析 (First Principles)
## 原始文件 (Original Document)
```

> **Language note**: The default is Traditional Chinese (繁體中文). To use a different language, update the note template in `tasks/ingest.md` and the style guide in `.agent/writing_style.md`.

---

## License

MIT — use it, fork it, make it yours.

---

*Built with [Claude Code](https://claude.ai/claude-code). The system scaffolding is public; personal knowledge notes are excluded via `.gitignore`.*
