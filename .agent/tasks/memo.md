# Task: Investment Memo
# Trigger: When user says "memo [company/theme]", "investment memo [topic]", or "memo --update [existing memo]"

> **Guiding Principles**: Apply `.agent/user_persona.md` — the dual consulting-investment lens is essential here. An investment memo should combine rigorous industry analysis (consulting DNA) with conviction-driven thesis formation (investor DNA). Apply Second-Level Thinking and First Principles Analysis throughout.

## Purpose

Structure a comprehensive investment memo from accumulated Garden research, or update an existing memo with new knowledge. This is where scattered research crystallizes into an actionable investment thesis with explicit conviction levels, catalysts, and risk assessment.

## Input

The user provides either:
- A new memo request: `memo TSMC`, `memo AI infrastructure theme`
- An update request: `memo --update 20_Projects/Investments/Memos/TSMC_Memo.md`

## Process

### Step 1: Gather Garden Research

Reuse the gathering logic from `tasks/brief.md` Steps 1-2:

1. Read `.agent/taxonomy.md` to understand the full category structure.
2. Identify all categories/subcategories relevant to the company or theme.
3. Scan notes in those areas. For each note, read frontmatter and content.
4. Also scan **adjacent categories** — a semiconductor memo should pull from AI_Infra, Geopolitics_Macro, Investment_Frameworks, etc.
5. Assess freshness: 🟢 Fresh (< 3 months), 🟡 Aging (3-6 months), 🔴 Stale (> 6 months or past review_by).
6. Collect all relevant notes (typically 15-40 for a comprehensive memo).

### Step 2: Check for Existing Memo

1. If `--update` flag is provided, read the existing memo.
2. If creating new, check `20_Projects/Investments/Memos/` for any prior memo on the same subject.
3. If an existing memo is found, note its last updated date and current conviction level.

### Step 3: Build the Memo (New)

For new memos, read the Investment_Memo.md template if available, then produce:

```markdown
---
title: [Company/Theme] 投資備忘錄
created: [today]
updated: [today]
review_by: [today + 3 months]
conviction: [High / Medium / Low]
status: active
tags: [relevant tags]
---

# [Company/Theme] 投資備忘錄

> 基於知識庫 [N] 篇相關筆記 | 最近更新：[today]

## 投資論點 (Investment Thesis)
[2-3 paragraphs synthesizing the core thesis from Garden research. This should be opinionated and specific — not "X is a good company" but "X will outperform because of [specific dynamic] over [specific timeframe]"]

## 關鍵論據 (Key Arguments)
1. **[Argument 1]** — 依據 [[Garden Note A]], [[Garden Note B]]
2. **[Argument 2]** — 依據 [[Garden Note C]]
3. **[Argument 3]** — 依據 [[Garden Note D]], [[Garden Note E]]

## 催化劑 (Catalysts)
[Near-term events or developments that could move the thesis forward]
| 催化劑 | 預期時間 | 影響程度 | 來源 |
|--------|----------|----------|------|
| [Catalyst 1] | [Timeline] | High/Med/Low | [[Note]] |
| [Catalyst 2] | [Timeline] | High/Med/Low | [[Note]] |

## 風險評估 (Risk Assessment)
[Apply assumption audit logic from tasks/challenge.md]

| # | 風險因素 | 可能性 | 影響 | 緩解因素 |
|---|----------|--------|------|----------|
| 1 | [Risk] | High/Med/Low | High/Med/Low | [Mitigation] |
| 2 | [Risk] | High/Med/Low | High/Med/Low | [Mitigation] |

### 最強空頭論點 (Strongest Bear Case)
[The single most compelling counter-argument, developed in 1-2 paragraphs]

## 估值框架 (Valuation Framework)
[Reference applicable models from Investment_Frameworks/Valuation_Models/]
- **適用模型**: [[Valuation Model Note]]
- **關鍵假設**: [key inputs and assumptions]
- **敏感度**: [what changes in assumptions would change the conclusion]

## 知識新鮮度 (Knowledge Freshness)
| 領域 | 筆記數 | 狀態 | 最近更新 |
|------|--------|------|----------|
| [Area 1] | N | 🟢/🟡/🔴 | YYYY-MM-DD |
| [Area 2] | N | 🟢/🟡/🔴 | YYYY-MM-DD |

## 信心水平與決策 (Conviction & Decision)
- **信心水平**: [High / Medium / Low] — [1-sentence justification]
- **建議動作**: [specific action recommendation]
- **重新評估觸發條件**: [what events should trigger memo review]

## 知識缺口 (Knowledge Gaps)
[What is NOT known that would materially affect the thesis?]
1. [Gap] — 建議研究：[specific research action]
2. [Gap] — 建議研究：[specific research action]
```

### Step 4: Update Existing Memo

For `--update` mode:

1. Diff current Garden knowledge against the existing memo's evidence base.
2. Identify: new supporting evidence, new contradicting evidence, changed assumptions, stale data points.
3. Produce an update summary:

```markdown
## 更新摘要 (Update Summary) — [today]

### 新增證據 (New Evidence)
- [[New Note]] — [how it affects the thesis]

### 變化的假設 (Changed Assumptions)
- 原假設：[old assumption] → 新觀點：[new view] — 依據 [[Note]]

### 信心調整建議 (Conviction Adjustment)
- 原信心：[old level] → 建議調整：[new level]
- 理由：[specific reason for change]
```

4. Update the memo's frontmatter (`updated`, `conviction` if changed, `review_by`).

### Step 5: Save Output

Save the completed memo to `20_Projects/Investments/Memos/[Company_Theme]_Memo.md`.

## Quality Checklist

- [ ] Thesis is opinionated and specific, not generic ("X is a good company")
- [ ] All key arguments cite specific Garden notes (not vague references)
- [ ] Risk assessment includes the strongest bear case, not strawmen
- [ ] Catalysts have specific timelines, not vague "in the future"
- [ ] Valuation framework references actual models from the knowledge base
- [ ] Knowledge freshness is assessed — stale data flagged prominently
- [ ] Knowledge gaps are specific and actionable
- [ ] For updates: diff is explicit and conviction adjustment is justified
- [ ] Language: Traditional Chinese with English technical terms
