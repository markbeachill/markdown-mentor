# Markdown Library Maker

Markdown Library Maker is the general-purpose part of the project.

It turns source files into one structured Markdown file. The file can then be pasted into an AI chatbot or used by another workflow.

## What it is for

Use it when you have several source files and want one clean file that keeps them separate and traceable.

Examples:

- teaching source packs
- research notes
- project documentation
- policy documents
- meeting notes
- writing research
- AI context packs

## Commands

Make a new library file:

```bash
markdown-library make ./sources -o my-library.md
```

Add more files later:

```bash
markdown-library add my-library.md ./new-sources
```

List the sources inside a library file:

```bash
markdown-library list my-library.md
```

Check the source markers:

```bash
markdown-library check my-library.md
```

## What the file contains

A Markdown library file contains:

- a short header
- the purpose, if you gave one
- source-start and source-end markers
- the original file name or path
- a source fingerprint
- the converted Markdown text

A source manifest is written next to the library file. It lists every file the tool found and says whether it was included or skipped.

## How Markdown Mentor uses it

Markdown Mentor uses the same file format for teaching. In the teaching workflow, the Markdown library file is also called an Educational Content Training Pack.
