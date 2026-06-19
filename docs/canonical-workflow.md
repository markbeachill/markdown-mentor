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

# Normal-user route

The normal user should not need to clone the repository or install the package.

The public website provides three downloadable Python files in:

```text
site/downloads/
  setup-markdown-mentor.py
  make-markdown-library.py
  make-teaching-materials.py
```

When published through GitHub Pages, these files are available at:

```text
https://markbeachill.github.io/markdown-mentor/downloads/setup-markdown-mentor.py
https://markbeachill.github.io/markdown-mentor/downloads/make-markdown-library.py
https://markbeachill.github.io/markdown-mentor/downloads/make-teaching-materials.py
```

For most users, the route is:

1. Make a new folder for the teaching project.
2. Download `setup-markdown-mentor.py` into that folder.
3. Run `python setup-markdown-mentor.py` from inside that folder.
4. The setup script downloads the two working scripts and creates the project folders.
5. The user puts source files in `1-source-files/`.
6. The user runs `python make-markdown-library.py make`.

The full package commands, such as `markdown-mentor new-project` and `make-markdown-library new`, are still available for developers and testers.

---

# The two tools

## Tool 1: Make Markdown Library

Command in the full package:

```text
make-markdown-library
```

Downloadable user script:

```text
make-markdown-library.py
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
existing Markdown library files
```

If a source folder contains an existing Markdown library file, the tool imports each source section from that library as a separate source. It does not add the old library as one large file. This keeps the new library readable to AI as a set of separate files.

By default, the tool does not add duplicate source fingerprints. Use `--allow-duplicates` only when you deliberately want duplicate sources. When a duplicate is skipped, the command prints:

```text
not added - filename
```

It creates and maintains:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

It does not decide whether the sources are good enough to teach from.

It only checks whether the Markdown library file is technically usable.

## Tool 2: Markdown Mentor

Command in the full package:

```text
markdown-mentor
```

Downloadable user script for the ordinary route:

```text
make-teaching-materials.py
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

Normal-user route:

```bash
python setup-markdown-mentor.py
```

This downloads the two working scripts and creates the project folders in the current folder.

Developer/tester route:

```bash
markdown-mentor new-project my-project
```

The user should work inside the project folder.

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
- existing Markdown library files

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

Normal-user command from inside the project folder:

```bash
python make-markdown-library.py make
```

This uses the default folders: source files from `1-source-files/`, output to `2-markdown-library/markdown-library.md`.

You can also give the source and destination explicitly:

```bash
python make-markdown-library.py make 1-source-files 2-markdown-library
```

The first folder is the source folder. The second folder is the destination folder.

Developer/tester command:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

Output:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

The tool should process folders, individual files, ZIP files, nested ZIP files, and existing Markdown library files.

If the source folder contains an existing Markdown library file, the tool should import the source sections from that library as separate sources in the new library. The old library file itself should not be added as one single source. This preserves the AI-readable structure: the new library still looks like a set of separate source files.

The Markdown library file contains the combined source material.

The manifest lists the files included in the library.

The library file should include a small metadata marker so the tool can recognise it later as a Markdown library file. This marker must not stop the AI reading the file as a normal set of source sections.

Duplicate rule:

- By default, do not add a source if its fingerprint is already in the library or already appeared earlier in the same run.
- If a duplicate is skipped, print `not added - filename`.
- If the user passes `--allow-duplicates`, add duplicates anyway.

The tool also checks that the file works technically. This means it checks things such as source sections, source boundaries, basic source information, and manifest generation.

This technical check does not decide whether the sources are good enough for teaching.

---

## Step 5. If needed, list or remove files from the Markdown library

The user may need to check what is inside the Markdown library.

Normal-user command:

```bash
python make-markdown-library.py list
```

Developer/tester command:

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

Normal-user command:

```bash
python make-markdown-library.py remove-file 3
```

Developer/tester command:

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

Project prompt files named `prompt-*.md` are ignored by the library builder. They are instructions for the user, not source material.

Duplicates are skipped by default. To deliberately include duplicates when making or adding sources, use:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md --allow-duplicates
```

or:

```bash
make-markdown-library add 2-markdown-library/markdown-library.md more-sources.zip --allow-duplicates
```

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
python make-teaching-materials.py export docx
```

Example PPTX export:

```bash
python make-teaching-materials.py export pptx
```

Example HTML export:

```bash
python make-teaching-materials.py export html
```

Example PDF export:

```bash
python make-teaching-materials.py export pdf
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
- files not added because they were duplicates

The Markdown library file should include a metadata marker, for example:

```text
<!-- markdown-library-file: true -->
```

The marker is for the tool. The rest of the library must remain plain, readable Markdown so AI can process it as a set of separate source sections.

The source number is used by:

Normal-user command:

```bash
python make-markdown-library.py remove-file 3
```

Developer/tester command:

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
