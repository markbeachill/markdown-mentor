# Markdown Mentor project folder

This folder keeps one teaching-material project in order.

## What goes where

`1-source-files/`
: Put the PDFs, Word files, slides, notes, readings, examples, ZIP files, and other source files here. The prompt file in this folder is ignored by the library builder.

`2-markdown-library/`
: The combined Markdown library file and manifest go here.

`3-teaching-approach/`
: Keep the editable teaching approach file here. It says what to teach, why, who it is for, and how to teach it.

`4-teaching-materials-pack/`
: Keep the editable teaching materials pack here. It says which teaching materials you want AI to create.

`5-draft-materials/`
: Save each AI-created Markdown teaching material here before export.

`6-final-exports/`
: Finished Word, PowerPoint, HTML, and PDF exports go here.

`style/`
: Keep the Markdown style file here. The default is `style/style.md`.

## First command

After you put source files into `1-source-files/`, run this from inside this project folder:

```bash
python make-markdown-library.py make
```

This uses the default folders: source files from `1-source-files/`, output to `2-markdown-library/markdown-library.md`.

You can also give the source and destination explicitly:

```bash
python make-markdown-library.py make 1-source-files 2-markdown-library
```

The first folder is the source folder. The second folder is the destination folder.

This creates:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

Developer/tester package command:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

## Next AI step

Upload `2-markdown-library/markdown-library.md` to your AI tool and use:

```text
3-teaching-approach/prompt-create-teaching-approach.md
```

Save the final approach as:

```text
3-teaching-approach/teaching-approach.md
```

## Export command

When your draft Markdown materials are saved in `5-draft-materials/`, run:

```bash
python make-teaching-materials.py export docx
```

Use `pptx`, `html`, or `pdf` instead of `docx` when you need another format.

Developer/tester package command:

```bash
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```
