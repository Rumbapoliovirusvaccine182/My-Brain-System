# Task: Ingest and Clean Data
# Trigger: When user says "Run Ingest" or "清洗 Inbox"

> **Guiding Principles**: Apply CLAUDE.md analysis mindset (dual-lens, "So What?" test, cross-industry connections) and `.agent/user_persona.md` quality framework.

> [!IMPORTANT]
> **CRITICAL RULES**:
> - **Process EACH file individually** — never consolidate multiple files into one note
> - **Never create "collection" or "batch" notes**
> - Each PDF/image/text file gets its own dedicated markdown note

# Universal Process for All Files (PDF, Image, Text/Markdown) in 00_Inbox:

1. **Analyze Content**:
   - **PDF**: For batch PDF extraction, run `python .agent/process_inbox.py` (no arguments). It extracts all PDFs to `.agent/inbox_content.json`. Then read the JSON for text content. For single PDFs, use the Read tool directly.
   - **Image**: Use the Read tool to analyze visually (Charts, Whiteboards) or transcribe text (Screenshots).
   - **Text/Markdown**: Read with Read tool. Clean formatting, remove noise (social media UI elements, timestamps), extract key concepts.

2. **Determine Category (Routing)**:
   - Read `.agent/taxonomy.md` to determine the best sub-folder (e.g., `AI_Tech`, `Investment`).
   - Let's call this `[Category]`.
   - **Check for Subcategories**: If `10_Garden/[Category]/` contains subdirectories (e.g., `AI_Hardware`, `AI_Products`), analyze the note content to determine the best subcategory.
   - Use keyword matching to route to the most appropriate subcategory.
   - Final path: `10_Garden/[Category]/[Subcategory]/` or `10_Garden/[Category]/` if no subcategories exist.

3. **Create Note**: Create a NEW `.md` file with a descriptive, semantic title.

4. **Structure & Analysis Framework (MANDATORY)**:
   You must STRICTLY follow this structure for all notes. Do not skip the "Key Insights" or "Related Concepts" sections.

   ```markdown
   ---
   title: [Descriptive Semantic Title]
   created: [YYYY-MM-DD]
   updated: [YYYY-MM-DD]
   review_by: [YYYY-MM-DD, created + 6 months]
   tags: [[Category], [Subcategory], [Keywords]]
   source_type: [pdf_report | image_capture | web_clipping]
   source_asset: [Original_Filename.ext]
   ---

   # [Title]

   ## 摘要 (Summary)
   [Concise high-level overview of the content. What is this file about?]

   ## 核心發現 (Core Findings)
   [Detailed analysis using H3 headers for key sections. Group related points together.]
   ### [Finding 1]
   - ...
   ### [Finding 2]
   - ...

   ## 相關概念連結 (Related Concepts)
   [List of WikiLinks to other relevant notes in the Garden. Add a brief description for each link.]
   **Apply user_persona principle**: Use the cross-industry lens to identify connections across categories (e.g., AI_Tech → Investment, Semiconductors → Materials).
   - [[Note A]] - [Brief relation]
   - [[Note B]] - [Brief relation]

   ## 關鍵洞察 (Key Insights)
   [A numbered list of 3-5 high-level takeaways or strategic implications. unique insights, not just facts.]
   **Apply user_persona principle**: Each insight must pass the "So What?" test and use strategic framing (implications for consulting/investment).
   1. **[Insight 1]**: ...
   2. **[Insight 2]**: ...
   3. **[Insight 3]**: ...

   ## 第二層思考 (Second-Level Thinking)
   [Go beyond surface-level observations. This is where competitive edge comes from.]
   **Guiding Questions**:
   - What are others NOT seeing in this information?
   - What are the second-order consequences of this trend/development?
   - What assumptions are embedded in the conventional wisdom, and are they valid?
   - What would need to be true for the consensus view to be wrong?
   - How might this play out differently than most expect?
   
   **Suggested Directions for Deeper Drilling**:
   - [Specific area to investigate further]
   - [Contrarian angle to explore]
   - [Adjacent domain to study for transferable insights]

   ## 第一性原理分析 (First Principles Analysis)
   [Break down to fundamental truths. Question assumptions. Rebuild from the ground up.]
   **Framework**:
   1. **What are we trying to achieve?** [Core objective/problem]
   2. **What do we know to be true?** [Fundamental facts, not assumptions]
   3. **What are we assuming?** [Identify and challenge each assumption]
   4. **Rebuild from fundamentals**: [New perspective based on first principles]
   
   **Example Application**:
   - Traditional view: [Conventional wisdom]
   - First principles breakdown: [Fundamental truths]
   - Reconstructed insight: [New conclusion from first principles]

   ## 原始文件 (Original Document)
   [Link to the archived source file]
   ![Source Asset](../../99_Archives/Assets/[Original_Filename.ext]) 
   *(Note: Ensure path is correct relative to the note's location)*
   ```

5. **Move & Archive**:
   - **Note**: Write the newly generated `.md` file to the determined path using the Write tool.
   - **Source Asset**: After all notes are written, move original source files from `00_Inbox/` to `99_Archives/Assets/` using bash `mv` commands. Rename to match the `[Semantic_Title]` (keeping original extension).

6. **Cleanup**: 
   - Remove any cached extraction files: `rm -f .agent/inbox_content.json`

# Final Report:
- List the processed files.
- State clearly: "Filed [Note Name] into [Category]/[Subcategory] folder."
- Confirm: "Source asset moved to Archives and renamed."

# Post-Processing Steps:
1. **Update Category Index**: Run `python .agent/generate_indices.py [CategoryName]` for each affected top-level category. This regenerates both Tier 1 and Tier 2 indices.
2. **Check Category Size**: If any leaf folder now exceeds 20 notes, inform user and suggest `@Agent sort-garden`.
3. **Gap Check**: If `.agent/gaps/` contains `active` gap reports, scan each newly ingested note against open gaps:
   - For each new note, determine which gap(s) it could fill based on the gap's description and fill criteria
   - If a match is found, report: "This note contributes to closing GAP-X: [gap name]"
   - Suggest `@Agent gaps --category [scope]` to refresh the report when multiple gaps have been filled
   - Do NOT auto-update gap report counters — only report matches.

---

# Quality Checklist

- [ ] **Cross-Domain WikiLinks**: WikiLinks to concepts in other categories?
- [ ] **"So What?" Test**: Each insight answers "Why does this matter?"
- [ ] **Dual-lens**: Framed for both consulting and investment implications?
- [ ] **Traditional Chinese**: Content in 繁體中文, English technical terms?
- [ ] **Context Awareness**: Checked for related existing Garden notes and linked?
- [ ] **Second-Level Thinking**: Non-obvious angles and second-order consequences identified?
