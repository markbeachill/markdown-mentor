"""Create a Markdown Mentor project folder.

A project folder gives users one clear place to keep sources, AI prompts,
draft materials, exports, and a Markdown style file.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_DIRS = [
    "1-source-files",
    "2-markdown-library",
    "3-teaching-approach",
    "4-teaching-materials-pack",
    "5-draft-materials",
    "6-final-exports",
    "style",
]

README_FIRST = """# Markdown Mentor project folder

This folder keeps one teaching-material project in order.

## What goes where

1-source-files/
: Put the PDFs, Word files, slides, notes, readings, examples, ZIP files, and other source files here.

2-markdown-library/
: Make Markdown Library saves the combined Markdown library file and manifest here.

3-teaching-approach/
: Keep the editable teaching approach file here. It says what to teach, why, who it is for, and how to teach it.

4-teaching-materials-pack/
: Keep the editable teaching materials pack here. It says which teaching materials you want AI to create.

5-draft-materials/
: Save each AI-created Markdown teaching material here before export.

6-final-exports/
: Markdown Mentor saves Word, PowerPoint, HTML, and PDF exports here.

style/
: Keep the Markdown style file here. The default is style/style.md.

## First command

After you put source files into 1-source-files, run this from inside this project folder:

```bash
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
```

The command creates:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

## Next AI step

Upload 2-markdown-library/markdown-library.md to your AI tool and use:

```text
3-teaching-approach/prompt-create-teaching-approach.md
```

Save the final approach as:

```text
3-teaching-approach/teaching-approach.md
```

## Export command

When your draft Markdown materials are saved in 5-draft-materials, run:

```bash
markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md
```

Use `pptx`, `html`, or `pdf` instead of `docx` when you need another format.
"""

DEFAULT_STYLE_MD = """# Style

This file controls how Markdown Mentor exports your finished teaching materials.
It is a Markdown file so you can read and edit it like the rest of the project.

The export tool uses the settings it understands. If a setting is unclear or unsupported, it uses the default.

## General style

- body_font: Calibri
- body_size_pt: 11
- heading_font: Calibri
- heading_color: 1F3864

## Word document style

- h1_size_pt: 20
- h2_size_pt: 16
- h3_size_pt: 13

## Slide style

- title_size_pt: 32
- body_size_pt: 20

## HTML style

- html_title: Teaching material

## PDF style

- use_docx_conversion: true
"""

PROMPT_FIND_MORE_SOURCES = """# Prompt: find more source materials

Use this prompt before you make the Markdown library if your source folder feels thin, narrow, or incomplete.

Paste this into your AI tool:

```text
I am building a source folder for a Markdown Mentor teaching-material project.

Here is what I already have, or what I think I have:
[Briefly describe the source files, topic, learner group, and anything I may want to teach.]

Please suggest useful extra source materials I could find, create, or add.

Focus on source materials, not finished teaching materials.

Suggest things like:
- worked examples
- comparison texts
- assessment criteria
- practice questions
- learner work
- background context
- glossary material
- diagrams or visual material
- beginner explanations

For each suggestion, explain why it would help and whether it is essential or optional.
Do not invent source titles or claim that you have seen files I have not provided. Suggest types of sources or places I might look.
```
"""

TEACHING_APPROACH = """# Teaching approach

## What to teach

Write the topic, text, concept, skill, or subject focus here.

## Aims of teaching

Write what learners should understand, practise, or be able to do after using the materials.

## Who is being taught

Write the learner group, level, age or stage if relevant, prior knowledge, needs, and context.

## How to teach

Write the teaching style, level of scaffolding, tone, practice style, feedback style, and any preferred pedagogy.
"""

PROMPT_CREATE_TEACHING_APPROACH = """# Prompt: create teaching approach

Use this prompt after you have made the Markdown library file.

Upload or paste:

```text
2-markdown-library/markdown-library.md
```

Then paste this prompt into your AI tool:

```text
I am using Markdown Mentor to create teaching materials from a Markdown library file.

Please help me create an editable teaching approach file with these sections:

# Teaching approach

## What to teach

## Aims of teaching

## Who is being taught

## How to teach

If I already say what I want to teach, turn that into a clear teaching approach file.
If I am not sure, suggest several possible teaching approaches that fit the source library, then ask me to choose or adapt one.

Use only what the library supports. If an idea would need extra sources or teacher-provided content, say so clearly.
Write in plain English.
```
"""

PROMPT_CHECK_TEACHING_APPROACH = """# Prompt: check teaching approach

Use this prompt after you have a draft teaching approach file.

Upload or paste:

```text
2-markdown-library/markdown-library.md
3-teaching-approach/teaching-approach.md
```

Then paste this prompt into your AI tool:

```text
Please check this teaching approach against the Markdown library.

Say:
- what the library supports well
- what the library only partly supports
- what would need more sources
- what would need teacher input
- whether the teaching approach should be narrowed or changed

If a gap cannot be supported by the library, say that it needs extra sources or teacher input.
End with a revised version of the teaching approach file if changes are needed.
```
"""

TEACHING_MATERIALS_PACK = """# Teaching materials pack

This file tells the AI what teaching materials to create.

Remove anything you do not need. Add anything that is missing.

## Materials to create

- Student handout
- Slide overview
- Worksheet with questions and answer guidance

## Notes

Write any length, format, or special requirements here.
"""

PROMPT_CREATE_TEACHING_MATERIALS = """# Prompt: create teaching materials

Use this prompt after the teaching approach and teaching materials pack are ready.

Upload or paste:

```text
2-markdown-library/markdown-library.md
3-teaching-approach/teaching-approach.md
4-teaching-materials-pack/teaching-materials-pack.md
```

Then paste this prompt into your AI tool:

```text
I am using Markdown Mentor to create teaching materials.

First, check whether the Markdown library has enough material, and the right type of material, for each requested output in the teaching materials pack.

For each requested output, mark it as one of:
- supported
- partly supported
- not supported
- needs teacher input
- needs extra sources

If the plan needs changing, suggest a revised materials pack before drafting.

After I accept or revise the plan, create each teaching material as a separate Markdown file.
Use clear filenames.
If a gap cannot be supported by the library, say that it needs extra sources or teacher input.
Write in plain English.
```
"""

@dataclass
class ProjectResult:
    path: Path
    created: list[Path]
    copied: list[Path]
    skipped: list[Path]


def _write(path: Path, text: str, *, overwrite: bool, copied: list[Path], skipped: list[Path]) -> None:
    if path.exists() and not overwrite:
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    copied.append(path)


def new_project(path: str | Path, *, overwrite: bool = False) -> ProjectResult:
    """Create a Markdown Mentor project folder."""
    project = Path(path).expanduser().resolve()
    created: list[Path] = []
    copied: list[Path] = []
    skipped: list[Path] = []

    if project.exists() and not project.is_dir():
        raise FileExistsError(f"A file already exists at {project}")

    project.mkdir(parents=True, exist_ok=True)
    created.append(project)

    for rel in PROJECT_DIRS:
        folder = project / rel
        folder.mkdir(parents=True, exist_ok=True)
        created.append(folder)

    _write(project / "README-FIRST.md", README_FIRST, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "1-source-files" / "prompt-find-more-source-materials.md", PROMPT_FIND_MORE_SOURCES, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "3-teaching-approach" / "teaching-approach.md", TEACHING_APPROACH, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "3-teaching-approach" / "prompt-create-teaching-approach.md", PROMPT_CREATE_TEACHING_APPROACH, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "3-teaching-approach" / "prompt-check-teaching-approach.md", PROMPT_CHECK_TEACHING_APPROACH, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "4-teaching-materials-pack" / "teaching-materials-pack.md", TEACHING_MATERIALS_PACK, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "4-teaching-materials-pack" / "prompt-create-teaching-materials.md", PROMPT_CREATE_TEACHING_MATERIALS, overwrite=overwrite, copied=copied, skipped=skipped)
    _write(project / "style" / "style.md", DEFAULT_STYLE_MD, overwrite=overwrite, copied=copied, skipped=skipped)

    return ProjectResult(path=project, created=created, copied=copied, skipped=skipped)
