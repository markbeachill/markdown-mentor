# Markdown Mentor

`markdown-mentor` is the teaching-material workflow tool.

It can:

```text
new-project
guide
export
```

## Create a project folder

```bash
markdown-mentor new-project my-project
```

This creates the numbered project folder and starter files.

## Show the workflow guide

```bash
markdown-mentor guide my-project
```

The guide tells the user which folders, files, and prompts to use. It does not send files to AI.

## Export draft materials

```bash
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```

Other formats:

```text
docx
pptx
html
pdf
```

PDF export needs LibreOffice.

The style file is Markdown and normally lives at:

```text
style/style.md
```
