# Task: Thesis Stress-Test (Challenge)
# Trigger: When user says "challenge [[Note]]", "stress test [[Note]]", or "challenge [topic]"

> **Guiding Principles**: Apply `.agent/user_persona.md` — specifically the "Second-Level Thinking" and "First Principles Analysis" frameworks. The user is a management consultant who values rigorous, non-obvious analysis.

## Purpose

Take an existing note (typically an investment thesis, industry analysis, or strategic position) and systematically attack it. Surface hidden assumptions, find contradicting evidence within the Garden, and construct the strongest possible bear case. The goal is to **make the user's thinking sharper**, not to be contrarian for its own sake.

## Input

The user provides either:
- A specific note: `challenge [[NVIDIA 多晶片策略]]`
- A topic/thesis: `challenge "AI hardware capex will keep growing through 2028"`

## Process

### Step 1: Extract the Thesis

1. If a note is specified, read it fully. Extract:
   - The **core thesis** (what is this note arguing?)
   - **Key assumptions** (what must be true for this thesis to hold?)
   - **Evidence cited** (what data/reasoning supports it?)
   - **Time horizon** (when is this expected to play out?)

2. If a topic is given, scan the Garden for relevant notes and reconstruct the user's implied thesis from accumulated knowledge.

### Step 2: Assumption Audit

List every assumption embedded in the thesis, including implicit ones. For each:

- **Assumption**: [Statement]
- **Confidence**: How well-supported is this in the Garden? (Strong / Moderate / Weak / Untested)
- **Fragility**: What would break this assumption? (Single event / Gradual shift / Black swan)

Common hidden assumptions to check:
- Market timing assumptions ("demand will grow because...")
- Competitive assumptions ("no one else can...")
- Technology assumptions ("this approach will scale...")
- Regulatory assumptions ("governments will/won't...")
- Macro assumptions ("rates/growth/policy will...")

### Step 3: Search for Contradictions

Scan the Garden for notes that contradict or complicate the thesis:
- Notes in the same subcategory with different conclusions
- Notes in adjacent categories that present counter-evidence
- Geopolitics_Macro notes that challenge industry-level assumptions
- Investment_Frameworks notes about cognitive biases that might apply

### Step 4: Pre-Mortem

Construct a narrative: **"It's 12 months later and this thesis completely failed. Here's what happened."**

Write this as a plausible story, not a laundry list. Include:
- The specific trigger event or trend that broke the thesis
- Why the evidence that seemed strong at the time turned out to be misleading
- What the user could have seen coming but didn't

### Step 5: Generate the Challenge

Output in Traditional Chinese:

```markdown
# 論點壓力測試: [Thesis Title]

> 基於 [[Original Note]] 及知識庫 [N] 篇相關筆記

## 核心論點摘要 (Thesis Summary)
[1-2 paragraphs restating the thesis being challenged]

## 假設審計 (Assumption Audit)

| # | 假設 | 支撐度 | 脆弱性 | 風險來源 |
|---|------|--------|--------|----------|
| 1 | [Assumption] | 🟢/🟡/🔴 | [What breaks it] | [Source] |
| 2 | ... | ... | ... | ... |

## 知識庫內部矛盾 (Evidence Against — From Your Own Notes)
[Most powerful section: quote specific notes that undermine the thesis]

- **[[Note A]]** 指出 "..." — 這與本論點的假設 #2 直接矛盾
- **[[Note B]]** 的數據顯示 ... — 暗示時間線可能比預期更長

## 事前驗屍 (Pre-Mortem)
> 想像現在是 [today + 12 months]，這個論點已經徹底失敗。

[2-3 paragraph narrative of how the thesis fell apart. Be specific, vivid, and plausible.]

## 最強空頭論點 (Strongest Bear Case)
[The single most compelling counter-argument, fully developed in 2-3 paragraphs]

## 什麼會改變你的想法 (What Would Change Your Mind)
[Specific, observable signals that should trigger thesis revision]
1. **轉為更看好的信號**: ...
2. **轉為看壞的信號**: ...
3. **需要更多資訊才能判斷**: ...

## 建議 (Recommendations)
- **如果維持原論點**: 應該監控 [specific metrics/events]
- **如果降低信心**: 考慮 [specific hedge or alternative]
- **知識缺口**: 需要研究 [specific area] 來解決假設 #N 的不確定性
```

## Quality Checklist

- [ ] Assumptions are genuinely hidden/implicit, not just restating obvious points
- [ ] Contradictions come from the user's OWN notes (most credible)
- [ ] Pre-mortem is a narrative (story), not a bullet list
- [ ] Bear case is the STRONGEST possible, not a strawman
- [ ] "What would change your mind" includes specific, observable triggers
- [ ] Challenge is respectful and constructive — goal is sharper thinking, not nihilism
- [ ] Language: Traditional Chinese with English technical terms
