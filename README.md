# Markdown Mentor

Markdown Mentor helps you turn source files into draft teaching materials with the help of AI, then export those materials to Word, PowerPoint, HTML, or PDF.

The project follows one source-of-truth workflow:

```text
docs/canonical-workflow.md
```

## Normal user route

Most users do not need to clone this repository or install the full package.

The website provides three downloadable Python files:

```text
site/downloads/setup-markdown-mentor.py
site/downloads/make-markdown-library.py
site/downloads/make-teaching-materials.py
```

When the site is published, they are available from:

```text
https://markbeachill.github.io/markdown-mentor/downloads/setup-markdown-mentor.py
https://markbeachill.github.io/markdown-mentor/downloads/make-markdown-library.py
https://markbeachill.github.io/markdown-mentor/downloads/make-teaching-materials.py
```

Normal workflow:

1. Make a new folder for a teaching project.
2. Download `setup-markdown-mentor.py` into that folder.
3. Run:

```bash
python setup-markdown-mentor.py
```

The setup file downloads the two working scripts and creates the project folders.

Then put source files in `1-source-files/` and run:

```bash
python make-markdown-library.py make
```

When draft Markdown teaching materials are ready in `5-draft-materials/`, export them:

```bash
python make-teaching-materials.py export docx
```

Use `pptx`, `html`, or `pdf` instead of `docx` when needed.

## What the setup file creates

```text
my-project/
  setup-markdown-mentor.py
  make-markdown-library.py
  make-teaching-materials.py
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

## The two tools

### Make Markdown Library

`make-markdown-library` is the general-purpose source tool in the package.

The normal-user script is:

```text
make-markdown-library.py
```

It turns source materials into one structured Markdown library file.

It works with folders, individual files, ZIP files, nested ZIP files, and existing Markdown library files. If it finds an existing library, it imports the sources inside it as separate sources, so AI can still read the new library as a set of files.

Normal-user commands:

```bash
python make-markdown-library.py make
python make-markdown-library.py add more-sources.zip
python make-markdown-library.py list
python make-markdown-library.py remove-file 3
python make-markdown-library.py check-file
```

Project prompt files named `prompt-*.md` are ignored by the library builder. They are instructions for the user, not source material.

Duplicates are skipped by default. If a duplicate is skipped, the tool prints `not added - filename`. Use `--allow-duplicates` only when you deliberately want duplicates.

### Markdown Mentor / teaching materials

`markdown-mentor` is the package command for the teaching-material workflow and export tool.

The normal-user script is:

```text
make-teaching-materials.py
```

Normal-user commands:

```bash
python make-teaching-materials.py guide
python make-teaching-materials.py export docx
python make-teaching-materials.py export pptx
python make-teaching-materials.py export html
python make-teaching-materials.py export pdf
```

PDF export needs LibreOffice. DOCX and PPTX export need the Python packages named in the error message if they are not already installed.

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

## Developer/tester route

The full repository is for development, testing, and maintaining the website.

Install from the repository folder:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Package commands are also available in this route:

```bash
markdown-mentor new-project my-project
markdown-mentor guide my-project
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```
