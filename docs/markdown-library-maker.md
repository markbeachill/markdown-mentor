# Make Markdown Library

Make Markdown Library is the general-purpose source tool.

It turns source files into one structured Markdown library file that an AI can read as a set of separate sources.

## Normal-user script

In the simple website route, users run:

```bash
python make-markdown-library.py make
```

This assumes the standard project folders:

```text
1-source-files/
2-markdown-library/
```

It creates:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

## Commands

```bash
python make-markdown-library.py setup
python make-markdown-library.py make
python make-markdown-library.py add more-sources.zip
python make-markdown-library.py list
python make-markdown-library.py remove-file 3
python make-markdown-library.py check-file
```

## Files it can work with

The tool can work with:

- folders
- individual files
- ZIP files
- nested ZIP files
- existing Markdown library files

If it finds an existing Markdown library file, it imports the source sections inside that library as separate sources. It does not add the old library as one large file. This keeps the new library readable to AI as a set of files.

## Duplicates

Project prompt files named `prompt-*.md` are ignored by the library builder. They are instructions for the user, not source material.

Duplicates are skipped by default.

If a duplicate is skipped, the tool prints:

```text
not added - filename
```

Use this only if you deliberately want duplicates:

```bash
python make-markdown-library.py make --allow-duplicates
```

or:

```bash
python make-markdown-library.py add more-sources.zip --allow-duplicates
```

## Remove a file

First list the files:

```bash
python make-markdown-library.py list
```

Then remove the file by number:

```bash
python make-markdown-library.py remove-file 3
```

The tool makes a backup before rewriting the library file.

## Developer/tester package command

The installed package also provides:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
make-markdown-library add 2-markdown-library/markdown-library.md more-sources.zip
make-markdown-library list 2-markdown-library/markdown-library.md
make-markdown-library remove-file 2-markdown-library/markdown-library.md 3
make-markdown-library check-file 2-markdown-library/markdown-library.md
```
