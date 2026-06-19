# Markdown Mentor workflow

The source of truth is:

```text
docs/canonical-workflow.md
```

## At a glance

### A. Create and develop your source materials library

1. Create a project folder with `setup-markdown-mentor.py`.
2. Collect source materials in `1-source-files/`.
3. If needed, use `1-source-files/prompt-find-more-source-materials.md`.
4. Run `python make-markdown-library.py make`.
5. If needed, use `python make-markdown-library.py list` and `python make-markdown-library.py remove-file 3`.

### B. Plan your teaching approach

6. Create or customise `3-teaching-approach/teaching-approach.md`.
7. Check it against the library with AI using `3-teaching-approach/prompt-check-teaching-approach.md`.
8. Choose or customise `4-teaching-materials-pack/teaching-materials-pack.md`.

### C. Create your teaching materials

9. Use AI and `4-teaching-materials-pack/prompt-create-teaching-materials.md` to create separate Markdown files in `5-draft-materials/`.
10. Choose or customise `style/style.md`.
11. Export with `python make-teaching-materials.py export docx` or another format.

## Rule

```text
Python checks files.
AI and the user check teaching fit.
```
