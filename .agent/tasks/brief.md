# Task: Situation Briefing
# Trigger: When user says "brief [topic]" or "briefing [topic]" or "brief me on [topic]"

> **Guiding Principles**: Apply `.agent/user_persona.md` — especially dual-purpose lens (consulting + investment), cross-industry connections, and "So What?" framing.

## Purpose

Synthesize everything the knowledge base knows about a topic into an actionable briefing. This is the compound interest on every note ever written — turning a scattered garden into a coherent strategic view.

## Input

The user provides a topic, question, or scenario. Examples:
- "brief NVIDIA's moat and competitive position"
- "brief me for a semiconductor client meeting"
- "brief 記憶體產業 current outlook"
- "What's my current view on AI infrastructure investment?"

## Process

### Step 1: Gather Relevant Notes

1. Read `.agent/taxonomy.md` to understand the full category structure.
2. Identify which categories/subcategories are relevant to the topic.
3. Scan notes in those areas. For each note, read frontmatter (title, tags, created, updated, review_by) and content.
4. Also scan **adjacent categories** for cross-domain connections (e.g., a brief on "CPO" should pull from Networking_Interconnect but also check AI_Infra, Semiconductor_Mfg, and Investment_Frameworks).
5. Collect 10-30 relevant notes depending on scope.

### Step 2: Assess Freshness

For each note pulled in:
- Check `updated` date against today.
- Flag notes where `review_by` date has passed as **potentially stale**.
- Distinguish between: 🟢 Fresh (updated < 3 months), 🟡 Aging (3-6 months), 🔴 Stale (> 6 months or past review_by).

### Step 3: Synthesize Briefing

Produce a structured briefing in Traditional Chinese (technical terms in English):

```markdown
# [Topic] 情勢簡報

> 基於知識庫 [N] 篇相關筆記，綜合日期 [today]

## 核心觀點 (Core Position)
[2-3 paragraphs synthesizing the knowledge base's accumulated view on this topic. Not a summary of individual notes — a unified, opinionated position built from all of them.]

## 關鍵論點 (Key Arguments)
[3-5 numbered arguments supporting the core position, each citing specific notes]
1. **[Argument]** — 依據 [[Note A]], [[Note B]]
2. ...

## 內部矛盾 (Internal Contradictions)
[Where do different notes disagree or present conflicting views? Be specific.]
- [[Note X]] 認為... 但 [[Note Y]] 指出...
- 這個矛盾的可能解釋：...

## 知識新鮮度 (Freshness Map)
| 領域 | 筆記數 | 狀態 | 最近更新 |
|------|--------|------|----------|
| [Sub-area 1] | N | 🟢/🟡/🔴 | YYYY-MM-DD |
| [Sub-area 2] | N | 🟢/🟡/🔴 | YYYY-MM-DD |

## 未解問題 (Open Questions)
[What does the knowledge base NOT cover about this topic? What assumptions remain untested?]
1. ...
2. ...

## 建議行動 (Recommended Actions)
[Based on the briefing, what should the user do next? Frame for both consulting and investment contexts where relevant.]
- **諮詢面**: ...
- **投資面**: ...
- **知識補充**: 建議深入研究 [specific gap]
```

### Step 4: Cross-Domain Connections

Before finalizing, explicitly check: are there insights from **other categories** (Journal, Parenting, Geopolitics_Macro) that shed unexpected light on this topic? Add a brief section if found.

## Quality Checklist

- [ ] Briefing synthesizes (not summarizes) — presents a unified view, not a list of note summaries
- [ ] Internal contradictions are surfaced honestly, not papered over
- [ ] Stale knowledge is flagged, not presented as current
- [ ] Open questions identify genuine gaps, not trivial ones
- [ ] Recommended actions are concrete and context-appropriate
- [ ] Cross-domain connections explored (user_persona: Knowledge as Graph)
- [ ] Language: Traditional Chinese with English technical terms
