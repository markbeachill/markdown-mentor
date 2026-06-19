# Make Markdown Library

`make-markdown-library` is the general-purpose source tool.

It turns a file, folder, ZIP, or nested ZIP into one structured Markdown library file.

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

Add more sources:

```bash
make-markdown-library add 2-markdown-library/markdown-library.md more-sources.zip
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
