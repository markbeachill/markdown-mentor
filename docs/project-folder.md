# Markdown Mentor project folder

A Markdown Mentor project is a normal folder with a fixed structure.

Create one with:

```bash
markdown-mentor new-project my-project
```

The folder looks like this:

```text
my-project/
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

## What each folder is for

| Folder | Purpose |
|---|---|
| `1-source-files/` | Put the source files you want to teach from here. |
| `2-markdown-library/` | The combined Markdown library file and manifest go here. |
| `3-teaching-approach/` | The editable teaching approach file and its AI prompts go here. |
| `4-teaching-materials-pack/` | The editable list of teaching outputs and its AI prompt go here. |
| `5-draft-materials/` | Save AI-created Markdown teaching materials here before export. |
| `6-final-exports/` | Save finished DOCX, PPTX, HTML, or PDF files here. |
| `style/` | Keep the Markdown style file here. The default is `style/style.md`. |

## Why prompts sit inside folders

Each prompt lives next to the file or task it helps with. For example, the prompt for the teaching approach lives in `3-teaching-approach/`, next to `teaching-approach.md`.

## Where examples live

Generic examples are on the website or in the repository library. They are not copied into every user project.

## Existing Markdown library files

If `1-source-files/` contains an existing Markdown library file, Make Markdown Library imports the source sections inside it as separate sources. It does not add the whole old library as one large file. Duplicates are skipped by default and reported as `not added - filename`.
