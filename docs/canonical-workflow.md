# Markdown Mentor Canonical Workflow

This document is the source of truth for the Markdown Mentor workflow.

All website pages, README instructions, starter project files, AI prompts, command examples, and guide text should follow this workflow.

---

# Core principle

Markdown Mentor separates source-file work from teaching-material work.

There are two tools:

1. **Make Markdown Library**  
   A general-purpose tool for turning source files into one Markdown library file.

2. **Markdown Mentor**  
   A teaching-material workflow tool that helps organise a project and export finished materials.

The AI helps with teaching judgement. The user remains in control.

The user chooses the sources, reviews AI suggestions, edits the teaching approach, approves the materials, and decides what to use.

The rule is:

```text
Python checks files.
AI and the user check teaching fit.
```

---

# The two tools

## Tool 1: Make Markdown Library

Command:

```text
make-markdown-library
```

This is a general-purpose tool. It is useful beyond Markdown Mentor.

It creates and manages a Markdown library file from source materials.

It can:

```text
new
add
list
remove-file
check-file
```

It can work with:

```text
folders
individual files
ZIP files
nested ZIP files
```

It creates and maintains:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

It does not decide whether the sources are good enough to teach from.

It only checks whether the Markdown library file is technically usable.

## Tool 2: Markdown Mentor

Command:

```text
markdown-mentor
```

This is the teaching-material workflow tool.

It can:

```text
new-project
guide
export
```

`new-project` creates a Markdown Mentor project folder.

`guide` shows the user the workflow steps in the terminal.

`export` converts finished Markdown teaching materials into styled output files.

---

# Project folder

A Markdown Mentor project is a working folder with the same structure every time.

```text
my-project/
  README-FIRST.md

  1-source-files/
    prompt-find-more-source-materials.md

  2-markdown-library/
    markdown-library.md
    markdown-library-manifest.md

  3-teaching-approach/
    teaching-approach.md
    prompt-create-teaching-approach.md
    prompt-check-teaching-approach.md

  4-teaching-materials-pack/
    teaching-materials-pack.md
    prompt-create-teaching-materials.md

  5-draft-materials/

  6-final-exports/

  style/
    style.md
```

## What each folder is for

| Folder | Purpose |
|---|---|
| `1-source-files/` | The source files the user wants to teach from. |
| `2-markdown-library/` | The combined Markdown library file and its manifest. |
| `3-teaching-approach/` | The editable file that says what to teach, why, who it is for, and how to teach it. |
| `4-teaching-materials-pack/` | The editable file that says which teaching materials to create. |
| `5-draft-materials/` | AI-created Markdown teaching materials go here before export. |
| `6-final-exports/` | Finished DOCX, PPTX, HTML, or PDF files go here. |
| `style/` | The editable Markdown style file used when exporting. |

---

# Workflow at a glance

## A. Create and develop your source materials library

1. Create a Markdown Mentor project folder.
2. Collect your source materials in the source folder.
3. If you need more source materials, ask AI what other source materials would be useful.
4. Make your Markdown library file.
5. If needed, list or remove files from the Markdown library.

## B. Plan your teaching approach

6. Create or customise your teaching approach file.
7. Check the teaching approach against the Markdown library with AI.
8. Choose and customise a teaching materials pack.

## C. Create your teaching materials

9. Ask AI to create the teaching materials as separate Markdown files.
10. Choose or customise your Markdown style file.
11. Process the teaching materials into styled output.

---

# A. Create and develop your source materials library

## Step 1. Create a Markdown Mentor project folder

Create a project folder before doing the work.

The project folder gives the user one place for source files, AI prompts, planning files, draft Markdown materials, the style file, and final exports.

Command:

```bash
markdown-mentor new-project my-project
```

Output:

```text
my-project/
```

The user should work inside this folder.

---

## Step 2. Collect your source materials in the source folder

Put the files you want to teach from in:

```text
1-source-files/
```

Source materials might include:

- Word documents
- PDFs
- PowerPoint slides
- Markdown files
- plain text notes
- HTML pages
- worksheets
- assessment criteria
- example answers
- learner writing, if it is safe and anonymised
- ZIP files containing any of the above

Example:

```text
1-source-files/
  orwell-politics-and-the-english-language.pdf
  notes-on-clear-writing.docx
  student-paragraphs.docx
  extra-readings.zip
```

---

## Step 3. If needed, ask AI what other source materials would be useful

This step is for users who think their source folder may be thin, narrow, or missing useful types of material.

Use this prompt:

```text
1-source-files/prompt-find-more-source-materials.md
```

The AI may suggest useful new source materials, such as worked examples, comparison texts, assessment criteria, practice questions, learner work, background context, glossary material, visual material, or beginner explanations.

The AI may suggest places or types of places to look. The user must still choose, check, and provide the actual sources.

This is not a Python check. It is an AI planning conversation.

---

## Step 4. Make your Markdown library file

Use Make Markdown Library to combine the source files into one Markdown library file.

Command:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

Output:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

The tool should process folders, individual files, ZIP files, and nested ZIP files.

The Markdown library file contains the combined source material.

The manifest lists the files included in the library.

The tool also checks that the file works technically. This means it checks things such as source sections, source boundaries, basic source information, and manifest generation.

This technical check does not decide whether the sources are good enough for teaching.

---

## Step 5. If needed, list or remove files from the Markdown library

The user may need to check what is inside the Markdown library.

Command:

```bash
make-markdown-library list 2-markdown-library/markdown-library.md
```

Example output:

```text
1. orwell-politics-and-the-english-language.pdf
2. notes-on-clear-writing.docx
3. old-duplicate-notes.docx
4. student-paragraphs.docx
```

To remove the third file:

```bash
make-markdown-library remove-file 2-markdown-library/markdown-library.md 3
```

The number comes from the list command.

After a file is removed, the tool should update:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

The tool should make a backup before rewriting the library file.

---

# B. Plan your teaching approach

## Step 6. Create or customise your teaching approach file

The teaching approach file is the main planning document.

It tells the AI what the user wants to teach and how the material should teach it.

File:

```text
3-teaching-approach/teaching-approach.md
```

The file should contain these sections:

```markdown
# Teaching approach

## What to teach

## Aims of teaching

## Who is being taught

## How to teach
```

The user can create this file in three ways:

1. write it directly
2. copy and edit an example from the website
3. ask AI to draft it from the Markdown library

If using AI, upload:

```text
2-markdown-library/markdown-library.md
```

Use this prompt:

```text
3-teaching-approach/prompt-create-teaching-approach.md
```

If the user already knows what they want to teach, the AI helps turn that idea into a clear teaching approach file.

If the user is not sure, the AI suggests possible teaching approaches from the Markdown library.

The website should show example teaching approach files.

---

## Step 7. Check the teaching approach against the Markdown library with AI

This is an AI conversation, not a Python command.

Upload or provide:

```text
2-markdown-library/markdown-library.md
3-teaching-approach/teaching-approach.md
```

Use this prompt:

```text
3-teaching-approach/prompt-check-teaching-approach.md
```

The AI should say:

- what the library supports well
- what the library only partly supports
- what would need more sources
- what would need teacher input
- whether the teaching approach should be narrowed or changed

If a gap cannot be supported by the library, the AI should say that it needs extra sources or teacher input.

The user should then edit and save the final version of:

```text
3-teaching-approach/teaching-approach.md
```

---

## Step 8. Choose and customise a teaching materials pack

A teaching materials pack tells the AI what files to create.

It is different from the teaching approach.

The teaching approach says what and how to teach.

The teaching materials pack says what outputs to make.

File:

```text
4-teaching-materials-pack/teaching-materials-pack.md
```

The user can create this file in three ways:

1. use the default pack
2. copy and edit an example pack from the website
3. write a custom pack

A teaching materials pack might ask for:

- student handout
- slide deck
- worksheet with questions and answer guidance
- quiz with answers
- tutor session materials
- revision materials
- self-study guide

The user can remove outputs they do not need and add outputs they do need.

The website should show example teaching materials packs.

---

# C. Create your teaching materials

## Step 9. Ask AI to create the teaching materials as separate Markdown files

Give the AI these inputs:

```text
2-markdown-library/markdown-library.md
3-teaching-approach/teaching-approach.md
4-teaching-materials-pack/teaching-materials-pack.md
```

Use this prompt:

```text
4-teaching-materials-pack/prompt-create-teaching-materials.md
```

The AI should first check whether the Markdown library has enough material, and the right type of material, for each requested output.

For each requested output, it should say one of:

- supported
- partly supported
- not supported
- needs teacher input
- needs extra sources

Then, after the user accepts or revises the plan, the AI should create each teaching material as a separate Markdown file.

Save the files in:

```text
5-draft-materials/
```

Example files:

```text
5-draft-materials/student-handout.md
5-draft-materials/slide-overview.md
5-draft-materials/worksheet-with-answer-guidance.md
```

These are draft teaching materials. The user should review and edit them before export.

---

## Step 10. Choose or customise your Markdown style file

The style file controls how the final exported files look.

File:

```text
style/style.md
```

The style file is Markdown so users can read and edit it like the other project files.

It may include sections such as:

```markdown
# Style

## General style

## Word document style

## Slide style

## HTML style

## PDF style
```

It can control or describe things such as fonts, heading sizes, spacing, slide appearance, document appearance, title pages, source notes, and how tables, lists, blockquotes, and code blocks should look.

The user can use the default style file, edit it, or create a new style file with the style builder.

The export tool should read this Markdown style file and apply the settings it understands. If a setting is unclear or unsupported, the tool should ignore it safely and use the default.

---

## Step 11. Process the teaching materials into styled output

When the draft Markdown materials are ready, export them.

Example DOCX export:

```bash
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```

Example PPTX export:

```bash
markdown-mentor export 5-draft-materials -f pptx -o 6-final-exports -s style/style.md
```

Example HTML export:

```bash
markdown-mentor export 5-draft-materials -f html -o 6-final-exports -s style/style.md
```

Example PDF export:

```bash
markdown-mentor export 5-draft-materials -f pdf -o 6-final-exports -s style/style.md
```

Final exported files are saved in:

```text
6-final-exports/
```

---

# Required project prompts

The project should include these prompts in the relevant folders.

```text
1-source-files/prompt-find-more-source-materials.md
3-teaching-approach/prompt-create-teaching-approach.md
3-teaching-approach/prompt-check-teaching-approach.md
4-teaching-materials-pack/prompt-create-teaching-materials.md
```

## prompt-find-more-source-materials.md

Used before the Markdown library is made.

Purpose:

To help the user identify useful new source materials to find, create, or add.

## prompt-create-teaching-approach.md

Used after the Markdown library is made.

Purpose:

To help create the teaching approach file.

The prompt should support two cases:

- the user already knows what they want to teach
- the user wants AI to suggest possible teaching approaches from the library

## prompt-check-teaching-approach.md

Used after the teaching approach file exists.

Purpose:

To check whether the teaching approach is supported by the Markdown library.

## prompt-create-teaching-materials.md

Used after the teaching approach and teaching materials pack exist.

Purpose:

To check whether the requested outputs are supported by the source library, then draft each teaching material as a separate Markdown file.

---

# Manifest rule

The Markdown library tool should generate and maintain a manifest.

The manifest should exist in two forms:

1. a source list inside the Markdown library file
2. a separate file:

```text
2-markdown-library/markdown-library-manifest.md
```

The manifest should include:

- source number
- source filename
- original path if available
- file type
- checksum or fingerprint
- conversion status
- warning notes if needed

The source number is used by:

```bash
make-markdown-library remove-file 2-markdown-library/markdown-library.md 3
```

---

# Website examples rule

Generic examples should be available on the website, not copied into every project folder.

The website should show examples of:

- teaching approach files
- teaching materials packs
- style files
- draft Markdown teaching materials
- exported outputs

Users can copy examples from the website if they want to customise them.

---

# Developer rules

If the workflow changes, update this canonical workflow document first.

Then update:

```text
README.md
docs/workflow.md
docs/project-folder.md
site/pages/workflow.html
site/pages/workflow/*.html
starter-project-template/README-FIRST.md
markdown_mentor/guide.py
library prompt templates
starter project template
```

Public-facing instructions should follow these rules:

```text
Python checks files.
AI and the user check teaching fit.
Prompts live where they are used.
Generic examples live on the website or in the repository, not in every project.
The style file is Markdown: style/style.md.
```
