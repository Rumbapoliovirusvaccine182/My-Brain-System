# Task: Auto-Subdivide Large Categories
# Trigger: Automatically called after "Sort Garden" or when a category exceeds threshold

> **Guiding Principles**: This workflow implements the universal principles defined in `.agent/user_persona.md`. When proposing subcategories, ensure they don't create silos that prevent cross-industry knowledge connections. Subcategories should facilitate navigation while maintaining the knowledge graph philosophy.

# Context:
You are the Structural Optimizer. After organizing notes into categories, you check if any category is too large and needs subdivision.

# Threshold Rules:
- **Small Category** (< 10 notes): Keep as single folder
- **Medium Category** (10-20 notes): Keep as single folder, monitor
- **Large Category** (> 20 notes): Propose subdivision
- **Very Large Category** (> 30 notes): Strongly recommend subdivision

# Steps:

## 1. Scan Categories
For each category in `10_Garden/` (e.g., AI_Tech, Investment):
- Count the number of `.md` files (excluding `主題索引.md`)
- If count > 20, flag for subdivision analysis

## 2. Analyze Flagged Categories
For each flagged category:
- Read all notes in the category
- Identify semantic clusters using keyword analysis
- Propose 2-4 logical subcategories
- Ensure balanced distribution (avoid 1 subcategory with 90% of notes)

## 3. Generate Subdivision Plan
Create a plan document: `[Category]_Subdivision_Plan.md`

Structure:
```markdown
# [Category] 細分方案

## 分析結果
| 子類別 | 筆記數 | 佔比 | 主題 |

## 建議的新結構
[Category]/
├── [Subcategory_1]/ (X 篇)
├── [Subcategory_2]/ (Y 篇)
└── [Subcategory_3]/ (Z 篇)

## 詳細分類
[List all files with their proposed subcategory]

## Action Required
如果同意此方案，請回覆：「@Agent Deploy [Category] Split」
```

## 4. Wait for Approval
- Present the plan to the user
- Do NOT execute subdivision without explicit approval
- User can modify the plan or reject it

## 5. Execute Subdivision (After Approval)
- Create subdirectories
- Move files to subcategories
- Generate `主題索引.md` for each subcategory
- Update parent category's `主題索引.md` to reference subcategories
- Delete the subdivision plan file

## 6. Generate Indices
- Call `tasks/generate_indices.md` for each new subcategory
- Update parent category index with navigation to subcategories

# Subdivision Criteria Examples:

## AI_Tech (29 notes) → 3 subcategories
- **AI_Hardware**: GPU/TPU/Trainium, NVIDIA, semiconductor
- **AI_Products**: Gemini TV, AR glasses, smart home
- **AI_Applications**: LLM applications, robotics, enterprise

## Investment (12 notes) → Keep as single category
- Below threshold, no subdivision needed

# Constraints:
- Maximum 4 subcategories per category (avoid over-fragmentation)
- Minimum 3 notes per subcategory (avoid too-small categories)
- Use semantic clustering, not alphabetical sorting
- Preserve all WikiLinks (update paths if needed)

# Integration Points:
- Called automatically at end of "Sort Garden" workflow
- Can be manually triggered: "@Agent Check Category Sizes"
- Results reported in final summary

# Quality Checklist (user_persona Compliance)

Before finalizing subdivision plan, verify:

- [ ] **Avoid Silos**: Do subcategories still allow cross-category WikiLinks? (user_persona: Knowledge Interconnection)
- [ ] **Strategic Clustering**: Are subcategories based on strategic themes, not just topics? (user_persona: Dual Purpose)
- [ ] **Balanced Distribution**: Does each subcategory have sufficient notes to be valuable? (user_persona: Structural Integrity)
- [ ] **Cross-Domain Potential**: Can notes in different subcategories still connect meaningfully? (user_persona: Core Philosophy)

---
# Example Output:

After "Sort Garden":
```
✅ Garden Restructured
📊 Category Analysis:
  - AI_Tech: 29 notes ⚠️ Exceeds threshold (20)
  - Investment: 12 notes ✅ Optimal size
  
🔍 Subdivision Recommended:
  - AI_Tech → Proposed 3 subcategories
  - See: AI_Tech_Subdivision_Plan.md for details
```
