# Install for testing

Markdown Mentor is still an early prototype. These instructions are for testers who are comfortable installing a Python tool.

## What gets installed

The install gives you two commands:

```text
make-markdown-library
markdown-mentor
```

`make-markdown-library` makes and manages Markdown library files.

`markdown-mentor` creates project folders, shows the workflow guide, and exports finished materials.

## Check Python

Open your command window and run:

```bash
python --version
```

You need Python 3.10 or newer.

If `python` does not work on Mac or Linux, try:

```bash
python3 --version
```

## Install this project for testing

From the repository folder, run:

```bash
pip install -e ".[dev]"
```

This installs Markdown Mentor and its Python dependencies, including MarkItDown.

## Create a test project

```bash
markdown-mentor new-project my-project
```

Put source files in:

```text
my-project/1-source-files/
```

Then from inside `my-project`, run:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

Then show the guide:

```bash
markdown-mentor guide my-project
```
