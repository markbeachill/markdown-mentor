# Install and setup notes

Markdown Mentor has two routes.

## Normal-user route

Most users should not clone the repository or install the package.

They should use the website download route:

1. Make a new folder for a project.
2. Download `setup-markdown-mentor.py` into that folder.
3. Run:

```bash
python setup-markdown-mentor.py
```

The setup file downloads:

```text
make-markdown-library.py
make-teaching-materials.py
```

Then it creates the project folders and starter files.

## Source conversion notes

The single-file script can read plain text, Markdown, HTML, and CSV files directly.

For Word, PowerPoint, PDF, and some other formats, it may need MarkItDown.

If the script says MarkItDown is needed, run:

```bash
python -m pip install "markitdown[all]"
```

Then run the library command again:

```bash
python make-markdown-library.py make
```

This uses the default folders: source files from `1-source-files/`, output to `2-markdown-library/markdown-library.md`.

You can also give the source and destination explicitly:

```bash
python make-markdown-library.py make 1-source-files 2-markdown-library
```

The first folder is the source folder. The second folder is the destination folder.

## Export notes

DOCX export may need:

```bash
python -m pip install python-docx
```

PPTX export may need:

```bash
python -m pip install python-pptx
```

PDF export needs LibreOffice.

## Developer/tester route

Developers and testers can install the package from the repository folder:

```bash
pip install -e ".[dev]"
```

Then run:

```bash
pytest
```
