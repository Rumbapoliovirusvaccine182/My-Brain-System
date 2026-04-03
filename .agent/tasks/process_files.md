# Task: Process Office Files
# Trigger: When user says "process files", "extract files", or drops Office files into a project folder

> **Guiding Principles**: Raw Office files (pptx, docx, xlsx, msg, eml, pdf) must be preprocessed into markdown + images before other workflows can use them. This is the bridge between the user's native work format and the system's markdown-based processing.

## Purpose

Convert Office format files into structured markdown with extracted images, so that `debrief`, `draft`, `prep`, and other workflows can read and process them. This preprocessor handles the format conversion; the downstream workflow handles the intelligence extraction.

## Input

The user specifies either:
- A single file: `process-files "Meetings/client_notes.docx"`
- A folder: `process-files "Meetings/"` (processes all supported files)
- A folder with recursion: `process-files "Research/" --recurse`

Supported formats: `.pptx`, `.docx`, `.xlsx`, `.msg`, `.eml`, `.pdf`

## Process

### Step 1: Run the Preprocessor

```bash
python .agent/process_files.py "path/to/file_or_folder" [--recurse]
```

For each file, the preprocessor creates a subfolder with:
- `content.md` — structured markdown (headings, bullet points, tables, image references)
- `img_001.png`, `img_002.png`, ... — extracted images, charts, graphs
- `metadata.md` — source file info, extraction date

### Step 2: Verify Extraction Quality

After preprocessing, quickly scan the output:
1. Does `content.md` contain readable structured text?
2. Were key images/charts extracted? (Check img_* count)
3. For PowerPoint: are slides clearly delineated?
4. For Excel: are tables properly formatted as markdown?
5. For Outlook: are metadata (sender, date, subject) captured?

If extraction quality is poor (e.g., scanned PDF with no text), flag to the user:
> "File `{{name}}` produced minimal text — it may be image-based. The extracted images are available for visual analysis."

### Step 3: Context-Specific Processing

Based on which project folder the file lives in, suggest the next workflow:

| Folder | File Types Expected | Next Workflow |
|--------|-------------------|---------------|
| **Meetings/** | .docx (notes), .msg/.eml (meeting invites/notes), .pdf (shared materials) | `debrief` — to extract decisions, actions, persona observations |
| **Research/** | .pdf (reports), .xlsx (data), .docx (analysis) | Read content.md for data; may feed into `draft` |
| **References/** | .pptx (past decks), .pdf (completed deliverables), .docx (past reports) | `draft` / `plan-project` — to learn structure, exhibits, approach |
| **Deliverables/** | .pptx (deck drafts), .pdf (exported decks) | `review-checklist` — to QC against personas |
| **00_Inbox/** | Any | `ingest` — for Garden knowledge processing |

### Step 4: Handle Email Attachments

For .msg/.eml files, the preprocessor may save attachments (e.g., a .pptx attached to a meeting invite). Flag these:
> "Email had {{N}} attachment(s) saved to `{{output_dir}}/`. Run `process-files` on them for extraction."

## Output

```
[OK] Processing complete:

Files processed: {{N}}
  - {{filename}} -> {{output_folder}}/ (content: X bytes, images: Y)
  - ...

Suggested next steps:
  - Meetings/ files: run `debrief` to extract decisions and action items
  - References/ files: content available for `draft` and `plan-project`
  - Research/ files: data tables extracted in content.md
```

## Quality Checklist

- [ ] All supported files in the target folder were processed
- [ ] Each file has a content.md with readable structured text
- [ ] Images/charts extracted where present in source files
- [ ] Email metadata (sender, date, subject) captured for .msg/.eml
- [ ] PowerPoint slides clearly numbered and delineated
- [ ] Excel tables properly formatted as markdown tables
- [ ] Email attachments flagged for separate processing
- [ ] Next workflow suggested based on folder context
