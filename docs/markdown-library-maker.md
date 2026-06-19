# Make Markdown Library

`make-markdown-library` is the general-purpose source tool.

It turns a file, folder, ZIP, nested ZIP, or existing Markdown library file into one structured Markdown library file.

It creates and maintains:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

The manifest lists the source files in the library. The list numbers can be used to remove a source later.

## Commands

Make a new library:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

If the source folder contains an existing Markdown library file, the tool imports the source sections from that library. It does not add the whole old library as one big source file. The new library still reads as a set of separate files for AI processing.

Duplicates are skipped by default. If a duplicate is skipped, the command prints `not added - filename`. To deliberately include duplicates, add `--allow-duplicates`:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md --allow-duplicates
```

Add more sources:

```bash
make-markdown-library add 2-markdown-library/markdown-library.md more-sources.zip
```

To add duplicates anyway:

```bash
make-markdown-library add 2-markdown-library/markdown-library.md more-sources.zip --allow-duplicates
```

List sources:

```bash
make-markdown-library list 2-markdown-library/markdown-library.md
```

Remove the third listed source:

```bash
make-markdown-library remove-file 2-markdown-library/markdown-library.md 3
```

Check the file structure:

```bash
make-markdown-library check-file 2-markdown-library/markdown-library.md
```

This check only checks that the Markdown library file is technically usable. It does not decide whether the source material is good enough for teaching.
