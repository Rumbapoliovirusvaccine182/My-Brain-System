# Task: Cross-Domain Discovery (Connect)
# Trigger: When user says "connect [[Note A]] [[Note B]]", "connect --discover [[Note]]", or "find connections for [topic]"

> **Guiding Principles**: Apply `.agent/user_persona.md` — this is the ultimate expression of "Knowledge as a Graph, Not an Archive." Cross-domain connections are the highest-value output of this system.

## Purpose

Discover non-obvious connections between concepts across different categories. Generate "bridge insights" — observations that only emerge at the intersection of two domains. This is the consultant's superpower: seeing patterns that domain specialists miss.

## Modes

### Mode 1: Connect Two Notes
`connect [[Note A]] [[Note B]]`

Given two specific notes (typically from different categories), find the structural, strategic, or conceptual bridge between them.

### Mode 2: Discover Connections for One Note
`connect --discover [[Note A]]`

Given a single note, scan the entire Garden for the most surprising and valuable connections.

### Mode 3: Topic Connection
`connect [topic A] [topic B]`

Given two topics/concepts, find notes that bridge them and synthesize the connection.

## Process

### Step 1: Extract Core Concepts

For each input note, extract:
- **Domain**: Which category/subcategory is it in?
- **Key concepts**: The 3-5 most important ideas or frameworks
- **Structural patterns**: What type of argument is it making? (e.g., supply-demand imbalance, platform strategy, technology adoption curve, competitive moat analysis)
- **Actors**: Companies, technologies, or forces involved
- **Dynamics**: What type of change or tension is described? (disruption, consolidation, scarcity, abundance, shift in power)

### Step 2: Pattern Matching

Search for structural similarities across the Garden:

**Level 1 — Direct keyword overlap**: Notes that share specific entities or technologies (obvious but still valuable).

**Level 2 — Structural analogy**: Notes that describe the same TYPE of dynamic in different domains. Examples:
- "Platform lock-in" in NVIDIA_Ecosystem ↔ "Platform lock-in" in AI_Applications (SaaS)
- "Supply scarcity driving pricing power" in Memory_Storage ↔ same dynamic in Commodities_Materials
- "Tiered resource allocation" in KV_Cache ↔ "Barbell strategy" in Investment_Frameworks

**Level 3 — Causal chain**: Notes where one's output is another's input. Examples:
- AI_Infra power demand → Clean_Energy investment opportunity
- Semiconductor_Mfg capacity constraints → AI_Chip_Alternatives emergence
- Geopolitics_Macro trade policy → specific supply chain note's assumptions

**Level 4 — Contrarian bridge**: Notes that seem to contradict each other but actually reveal a deeper truth when reconciled.

### Step 3: Generate Bridge Insights

For each connection found (aim for 3-5), produce:

```markdown
### 連結 [N]: [Connection Title]

**筆記 A**: [[Note A Title]] ([Category])
**筆記 B**: [[Note B Title]] ([Category])

**連結類型**: [Direct / Structural Analogy / Causal Chain / Contrarian Bridge]

**橋接洞察 (Bridge Insight)**:
[2-3 paragraphs explaining the connection. This must be a NEW insight that doesn't exist in either note alone. It should feel like a genuine "aha!" moment.]

**實戰意義 (Practical Implications)**:
- **諮詢面**: [How this connection helps in client work]
- **投資面**: [How this connection informs investment decisions]

**建議行動**:
- 在 [[Note A]] 新增連結到 [[Note B]]，附註: [specific context]
- 在 [[Note B]] 新增連結到 [[Note A]]，附註: [specific context]
- [Optional: suggest a new note that explores this intersection]
```

### Step 4: Output

```markdown
# 跨域連結發現: [Topic/Notes]

> 掃描範圍: [N] 篇筆記 | 發現 [M] 個連結 | 日期: [today]

## 連結總覽

| # | 類型 | 筆記 A | 筆記 B | 橋接洞察 |
|---|------|--------|--------|----------|
| 1 | [Type] | [[...]] | [[...]] | [One-line insight] |

## 詳細連結分析

[Step 3 output for each connection]

## 最有價值的發現 (Top Insight)
[Highlight the single most surprising/valuable connection with extended analysis]

## 建議的 WikiLink 更新
[Consolidated list of all WikiLinks to add, ready for execution]

## 探索方向 (Further Exploration)
[Suggest 2-3 additional connection searches worth running]
```

## Quality Checklist

- [ ] Bridge insights are genuinely NEW — not just "these two notes are both about AI"
- [ ] At least one connection is cross-category (not just within Investment/)
- [ ] Structural analogies are specific ("both use tiered allocation") not vague ("both are about strategy")
- [ ] Practical implications are concrete for consulting AND investment
- [ ] WikiLink suggestions are ready to execute
- [ ] The "Top Insight" is genuinely surprising — something the user likely hasn't thought of
- [ ] Language: Traditional Chinese with English technical terms
