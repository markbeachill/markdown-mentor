# Markdown Mentor tool

Markdown Mentor is the teaching-material workflow and export part of the project.

The normal-user route uses the downloadable script:

```text
make-teaching-materials.py
```

It does not send files to AI. The user runs the AI prompts in their own AI tool.

## Normal-user commands

Show the workflow:

```bash
python make-teaching-materials.py guide
```

Export draft Markdown materials from `5-draft-materials/` into `6-final-exports/`:

```bash
python make-teaching-materials.py export docx
python make-teaching-materials.py export pptx
python make-teaching-materials.py export html
python make-teaching-materials.py export pdf
```

The style file is:

```text
style/style.md
```

## Developer/tester package command

The installed package also provides:

```bash
markdown-mentor new-project my-project
markdown-mentor guide my-project
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```

`new-project` creates a project folder.

`guide` shows the workflow steps in the terminal.

`export` converts finished Markdown teaching materials into styled output files.

## Rule

Markdown Mentor does not judge whether sources are good enough to teach from in Python.

Teaching judgement belongs to the AI prompts and the user's review.
