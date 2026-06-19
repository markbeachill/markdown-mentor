# The Markdown Mentor workflow, step by step

This page walks through the whole workflow once, using the sample files in this
project. By the end you will have turned a small folder of sources into a Word
handout, a slide deck, and a web page.

## What this page is about

A complete run through Markdown Mentor, from a folder of files to finished,
exported teaching materials.

## Why it matters

Seeing the whole chain once makes each step clear. After this, you can do the
same with your own files.

## What you should do next

Work through the steps in order. Each step says who does what: you, Markdown
Mentor, or the AI.

---

## Before you start

Install MarkItDown (see `install-markitdown.md`) and Markdown Mentor (see the
README). Open a terminal in the `markdown-mentor` folder.

There is a shortcut for everything below. The guided command runs the software
steps for you and points you to the right prompt at each AI step:

```bash
markdown-mentor start
```

It asks for your sources folder, builds and checks the pack, then walks you
through the rest one step at a time. The steps below explain each part in full.

## Step 1: Collect sources (you)

For this walkthrough, the sources are already provided in
`examples/sample-sources`. They are three short files about thesis statements.

For your own work, you would gather your files into one folder. See
`library/source-guides/collecting-sources.md` for what makes a good set.

## Step 2: Build the content pack (Markdown Mentor)

Run:

```bash
markdown-mentor build-pack examples/sample-sources -g "teach thesis statements to sixth-form students"
```

Markdown Mentor converts each file and writes two files: `content-pack.md` (the
pack itself) and `content-pack-manifest.md` (a list of every file it found).
The content pack is the file you will paste into an AI chatbot later.

## Step 3: Check the pack (Markdown Mentor)

Run:

```bash
markdown-mentor check-pack content-pack.md -g "teach thesis statements to sixth-form students"
```

This writes `content-pack-readiness.md`. Read it. It may warn that the sample
pack is short. That is expected: the samples are tiny. With your own fuller
sources, the warnings will guide you on what to add.

If you want help deciding what to add, paste the "improve the content pack"
prompt (`library/prompts/improve-content-pack.md`) into a chatbot, then paste
your pack.

## Step 4: Decide what to teach (you, with the AI)

Either write a Teaching Brief yourself (see
`library/teaching-briefs/sample-teaching-brief.md` for the shape), or paste the
"suggest teaching briefs" prompt into a chatbot, paste your content pack, and
edit one of the suggestions it gives you.

## Step 5: Choose how to teach it (you)

Pick a Pedagogy Specification from `library/pedagogy-specs`. For this
walkthrough, use `school-level.md`. Edit it if you want a different tone or
amount of support.

## Step 6: Choose which materials to make (you)

Pick a Teaching Materials List from `library/materials-lists`. For this
walkthrough, use `getting-started.md`.

## Step 7: Plan the materials (the AI), then check the plan (you)

Open the "generate inventory" prompt (`library/prompts/generate-inventory.md`).
Paste it into a chatbot, then paste, where the prompt asks: your content pack,
your Teaching Brief, your Pedagogy Specification, the Teaching Material
Specifications (`library/material-specs/teaching-material-specifications.md`),
and your Teaching Materials List.

The AI returns a Teaching Materials Inventory: a numbered plan. Read it. This is
the main checkpoint. Fix the plan now if it is wrong: it is far easier than
fixing many finished documents.

## Step 8: Generate each material (the AI), one at a time

For each item in the inventory, open the "generate material" prompt
(`library/prompts/generate-material.md`). Paste it into a chatbot, then paste
your content pack, your Pedagogy Specification, the matching Teaching Material
Specification, and the one inventory item.

The AI returns one material in Markdown. Read it and edit anything that is
wrong. Save it as a `.md` file in a folder, for example `materials/`.

Repeat for each item. One file per material keeps things easy to check and redo.

## Step 9: Export (Markdown Mentor)

Turn your Markdown materials into the formats people use. To convert a whole
folder to Word:

```bash
markdown-mentor export materials -f docx -o exports
```

To make slides or a web page, change the format:

```bash
markdown-mentor export materials -f pptx -o exports
markdown-mentor export materials -f html -o exports
```

To control the look, add a style profile:

```bash
markdown-mentor export materials -f docx -o exports -s library/style-profiles/student-handout.json
```

## Done

You now have finished teaching materials in Word, PowerPoint, and web formats.
To make a PDF, use `-f pdf`. PDF export uses LibreOffice (a free office suite)
if you have it installed:

```bash
markdown-mentor export materials -f pdf -o exports
```

If you do not have LibreOffice, the tool will tell you, and you can open the
Word or web file and use "Save as PDF" in your own software instead.

## A note on trust

The AI can draft quickly, but it can also be wrong. Always read what it
produces. The "Sources used" section the prompts ask for helps you check that a
material is grounded in your own content.
