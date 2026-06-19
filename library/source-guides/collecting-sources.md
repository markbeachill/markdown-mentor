# How to collect good sources

The quality of your teaching materials depends on the quality of your sources.
This guide helps you put together a source folder for a Markdown Mentor project.

## Why this matters

If your sources are thin, out of date, or contradictory, the materials the AI makes will have the same problems. A little care here saves a lot of editing later.

## What to put in

Aim to include a useful mix of:

- **Core explanations.** Clear writing that explains the topic.
- **Examples.** Worked examples show how the idea is used.
- **Activities and questions.** Practice material shows the kind of task you want.
- **Assessment material.** Mark schemes or success criteria, if you have them.
- **Learner-level information.** A note of who this is for and their level.
- **Curriculum or exam requirements.** If your teaching must match a syllabus.
- **ZIP files.** Make Markdown Library can unpack ZIP files and nested ZIP files.
- **Existing Markdown library files.** If you already have a Markdown library file, put it in the source folder. The tool will import the sources inside it as separate sources.

## What to leave out

- **Duplicates.** The same file twice can skew the result.
- **Out-of-date files.** Old versions confuse the picture.
- **Private student data.** Never include names, contact details, ID numbers, or anything that identifies a real learner. Remove or anonymise it first.
- **Copyrighted material you may not use.** Only include material you have permission to use.
- **Background reading you will not teach from.** Wide reading that is not about your topic adds noise.

## If the folder feels thin

Use:

```text
1-source-files/prompt-find-more-source-materials.md
```

The AI can suggest useful kinds of source material to find, create, or add. It may suggest examples, comparison texts, assessment criteria, practice questions, learner work, background context, glossary material, visual material, or beginner explanations.

The AI does not provide the sources for you. You still choose, check, and add the actual files.

## A simple way to start

1. Create a project folder.
2. Put your best source files in `1-source-files/`.
3. Make sure at least one file explains the idea and at least one gives an example.
4. Remove anything private.
5. Make the Markdown library file.
6. Use the teaching approach prompt to decide what this library can support.

## File types that work

Make Markdown Library can read text, Markdown, Word, PDF, PowerPoint, HTML, CSV, ZIP files, nested ZIP files, and existing Markdown library files. If a file will not convert, save it as a Word document or PDF and try again.

## Duplicates

Duplicates are skipped by default using the source fingerprint. If the tool skips a duplicate, it prints `not added - filename`. Use `--allow-duplicates` only when you deliberately want duplicate sources in the library.
