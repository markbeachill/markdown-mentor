# Markdown Mentor

Markdown Mentor is the education-focused part of the project.

It starts with a Markdown library file and helps you turn that source material into teaching and learning materials.

## What it does

Markdown Mentor can:

- guide you through the teaching workflow
- check whether a source library is strong enough for a teaching goal
- point you to prompts for teaching briefs, inventories, and generated materials
- export finished Markdown materials to DOCX, PPTX, HTML, or PDF

## Main commands

Start the guided workflow:

```bash
markdown-mentor start
```

Check a library/content pack for teaching use:

```bash
markdown-mentor check-pack my-library.md -g "teach thesis statements"
```

Export finished materials:

```bash
markdown-mentor export ./materials -f docx
```

Teaching alias for making a content pack:

```bash
markdown-mentor build-pack ./sources
```

For general source libraries, prefer:

```bash
markdown-library make ./sources -o my-library.md
```

## What Markdown Mentor does not do

Markdown Mentor does not talk to an AI API. You use the prompts in your own AI chatbot and check the output yourself.
