# Markdown Mentor project folder

A Markdown Mentor project is one ordinary folder. The normal route is to download one setup file into a new folder and run it there.

## Normal-user setup

1. Make a new folder for your project.
2. Download `setup-markdown-mentor.py` into that folder from the website.
3. Open a command window in that folder.
4. Run:

```bash
python setup-markdown-mentor.py
```

The setup file downloads:

```text
make-markdown-library.py
make-teaching-materials.py
```

It then creates:

```text
README-FIRST.md
1-source-files/
2-markdown-library/
3-teaching-approach/
4-teaching-materials-pack/
5-draft-materials/
6-final-exports/
style/style.md
```

It only changes the folder where you run it. It does not upload your files.

## Project structure

```text
my-project/
  setup-markdown-mentor.py
  make-markdown-library.py
  make-teaching-materials.py
  README-FIRST.md

  1-source-files/
    prompt-find-more-source-materials.md

  2-markdown-library/
    markdown-library.md
    markdown-library-manifest.md

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

## First project command

After putting source files into `1-source-files/`, run:

```bash
python make-markdown-library.py make
```

This creates:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

## Developer/tester route

Developers can still use the installed package command:

```bash
markdown-mentor new-project my-project
```
