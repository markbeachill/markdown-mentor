# Markdown Mentor

Markdown Mentor helps you turn source files into draft teaching materials with the help of AI, then export those materials to Word, PowerPoint, HTML, or PDF.

The project follows one source-of-truth workflow:

```text
docs/canonical-workflow.md
```

## The two tools

### Make Markdown Library

`make-markdown-library` is the general-purpose source tool. It turns source materials into one structured Markdown library file.

It works with folders, individual files, ZIP files, nested ZIP files, and existing Markdown library files. If it finds an existing library, it imports the sources inside it as separate sources, so AI can still read the new library as a set of files.

Common commands:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
make-markdown-library add 2-markdown-library/markdown-library.md more-sources.zip
make-markdown-library list 2-markdown-library/markdown-library.md
make-markdown-library remove-file 2-markdown-library/markdown-library.md 3
make-markdown-library check-file 2-markdown-library/markdown-library.md
```

### Markdown Mentor

`markdown-mentor` is the teaching-material workflow and export tool.

Common commands:

```bash
markdown-mentor new-project my-project
markdown-mentor guide my-project
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```

`guide` shows the workflow in the terminal. It does not send anything to AI.

## Start a project

Create a project folder:

```bash
markdown-mentor new-project my-project
```

This creates:

```text
my-project/
  README-FIRST.md
  1-source-files/
    prompt-find-more-source-materials.md
  2-markdown-library/
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

Put your source files in `1-source-files/`, then run this from inside the project folder:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

Duplicates are skipped by default. If a duplicate is skipped, the tool prints `not added - filename`. Use `--allow-duplicates` only when you deliberately want duplicates.

The tool also creates:

```text
2-markdown-library/markdown-library-manifest.md
```

## AI steps

The AI steps happen in your own AI tool. Markdown Mentor does not send files to AI.

Use the prompt files in the folder where they are needed:

```text
1-source-files/prompt-find-more-source-materials.md
3-teaching-approach/prompt-create-teaching-approach.md
3-teaching-approach/prompt-check-teaching-approach.md
4-teaching-materials-pack/prompt-create-teaching-materials.md
```

The key rule is:

```text
Python checks files.
AI and the user check teaching fit.
```

## Export

When the AI-created Markdown files are saved in `5-draft-materials/`, export them:

```bash
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```

Use `pptx`, `html`, or `pdf` instead of `docx` when needed.

PDF export needs LibreOffice.

## Install for testing

This is still an early prototype. For now, testers should install from the repository folder:

```bash
pip install -e ".[dev]"
```

Then run:

```bash
pytest
```
