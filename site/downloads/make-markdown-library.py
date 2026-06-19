#!/usr/bin/env python3
"""Make a Markdown library file from source files.

Normal use from inside a Markdown Mentor project folder:

    python make-markdown-library.py setup
    python make-markdown-library.py make
    python make-markdown-library.py make 1-source-files 2-markdown-library
    python make-markdown-library.py list
    python make-markdown-library.py remove-file 3

This is a single-file user script. It uses only the current folder unless you
provide other paths. It does not upload your files.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

DELIMITER = "=" * 70
LIBRARY_MARKER = "<!-- markdown-library-file: true -->"
DEFAULT_SOURCE_DIR = Path("1-source-files")
DEFAULT_LIBRARY = Path("2-markdown-library/markdown-library.md")

SUPPORTED_SUFFIXES = {
    ".txt", ".md", ".markdown", ".html", ".htm", ".csv",
    ".docx", ".doc", ".pdf", ".pptx", ".ppt",
}

README_FIRST = """# Markdown Mentor project folder

This folder keeps one teaching-material project in order.

## First steps

1. Put your source files in `1-source-files/`.
2. Make the Markdown library file:

```bash
python make-markdown-library.py make
```

This creates:

```text
2-markdown-library/markdown-library.md
2-markdown-library/markdown-library-manifest.md
```

3. Upload `2-markdown-library/markdown-library.md` to your AI tool.
4. Use `3-teaching-approach/prompt-create-teaching-approach.md`.
5. Save the final approach as `3-teaching-approach/teaching-approach.md`.

When your draft Markdown materials are saved in `5-draft-materials/`, export them:

```bash
python make-teaching-materials.py export docx
```

Use `pptx`, `html`, or `pdf` instead of `docx` if needed.
"""

PROMPT_FIND_MORE = """# Prompt: find more source materials

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

PROMPT_CREATE_APPROACH = """# Prompt: create teaching approach

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

PROMPT_CHECK_APPROACH = """# Prompt: check teaching approach

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

MATERIALS_PACK = """# Teaching materials pack

This file tells the AI what teaching materials to create.

Edit the list below. Remove anything you do not need. Add anything that is missing.

## Materials to create

- Student handout
- Slide overview
- Worksheet with questions and answer guidance

## Notes

Keep each finished teaching material as a separate Markdown file.
"""

PROMPT_CREATE_MATERIALS = """# Prompt: create teaching materials

Use this prompt after you have:

```text
2-markdown-library/markdown-library.md
3-teaching-approach/teaching-approach.md
4-teaching-materials-pack/teaching-materials-pack.md
```

Paste this prompt into your AI tool:

```text
I am using Markdown Mentor to create teaching materials.

Use these inputs:
- the Markdown library
- the teaching approach file
- the teaching materials pack

First, check whether the library has enough material, and the right type of material, for each requested output.

For each output, mark it as one of:
- supported
- partly supported
- not supported
- needs teacher input
- needs extra sources

If anything needs changing, suggest a revised materials pack before generating.

After I approve the plan, create each teaching material as a separate Markdown file.
Use clear headings.
Keep source-grounded claims traceable to the library.
Write in plain English.
```
"""

STYLE_MD = """# Style

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


@dataclass
class Record:
    name: str
    path: str
    suffix: str
    size: int
    fingerprint: str
    included: bool
    note: str = ""


def write_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def setup_project(root: Path) -> None:
    for folder in [
        "1-source-files", "2-markdown-library", "3-teaching-approach",
        "4-teaching-materials-pack", "5-draft-materials", "6-final-exports", "style",
    ]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    write_if_missing(root / "README-FIRST.md", README_FIRST)
    write_if_missing(root / "1-source-files/prompt-find-more-source-materials.md", PROMPT_FIND_MORE)
    write_if_missing(root / "3-teaching-approach/teaching-approach.md", TEACHING_APPROACH)
    write_if_missing(root / "3-teaching-approach/prompt-create-teaching-approach.md", PROMPT_CREATE_APPROACH)
    write_if_missing(root / "3-teaching-approach/prompt-check-teaching-approach.md", PROMPT_CHECK_APPROACH)
    write_if_missing(root / "4-teaching-materials-pack/teaching-materials-pack.md", MATERIALS_PACK)
    write_if_missing(root / "4-teaching-materials-pack/prompt-create-teaching-materials.md", PROMPT_CREATE_MATERIALS)
    write_if_missing(root / "style/style.md", STYLE_MD)


def checksum_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def checksum_text(text: str) -> str:
    normal = re.sub(r"\s+", " ", text).strip().encode("utf-8")
    return checksum_bytes(normal)


def safe_extract_zip(zip_path: Path, extract_to: Path) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        root = extract_to.resolve()
        for member in zf.infolist():
            target = (extract_to / member.filename).resolve()
            if not str(target).startswith(str(root)):
                raise zipfile.BadZipFile("ZIP contains an unsafe file path")
        zf.extractall(extract_to)


def gather_files(source: Path, work_dir: Path) -> list[Path]:
    found: list[Path] = []

    def handle_file(path: Path) -> None:
        if path.suffix.lower() == ".zip":
            target = work_dir / f"{path.stem}_unzipped"
            target.mkdir(parents=True, exist_ok=True)
            try:
                safe_extract_zip(path, target)
                walk(target)
            except zipfile.BadZipFile:
                found.append(path)
        else:
            found.append(path)

    def walk(folder: Path) -> None:
        for item in sorted(folder.rglob("*")):
            if item.is_file():
                handle_file(item)

    if source.is_dir():
        walk(source)
    elif source.is_file():
        handle_file(source)
    else:
        raise FileNotFoundError(f"Source not found: {source}")
    return found


def relative_to_source(path: Path, source: Path) -> str:
    try:
        base = source if source.is_dir() else source.parent
        return str(path.relative_to(base))
    except ValueError:
        return path.name


def is_library_text(text: str) -> bool:
    return LIBRARY_MARKER in text or ("SOURCE START" in text and "SOURCE END:" in text and "Fingerprint:" in text)


def is_manifest_text(text: str) -> bool:
    return "# Markdown Library Manifest" in text and "| No. | File |" in text


def parse_sections(text: str) -> list[dict[str, str]]:
    pattern = re.compile(
        rf"{re.escape(DELIMITER)}\nSOURCE START\nFile: (?P<file>.*?)\nFingerprint: (?P<fp>.*?)\n{re.escape(DELIMITER)}\n(?P<body>.*?)\n{re.escape(DELIMITER)}\nSOURCE END: .*?\n{re.escape(DELIMITER)}",
        re.DOTALL,
    )
    sections = []
    for m in pattern.finditer(text):
        sections.append({"file": m.group("file"), "fingerprint": m.group("fp"), "body": m.group("body").strip(), "raw": m.group(0)})
    return sections


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()


def read_plain(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        return strip_html(text)
    return text.strip()


def convert_with_markitdown(path: Path) -> str:
    from markitdown import MarkItDown  # type: ignore
    md = MarkItDown()
    result = md.convert(str(path))
    return (result.text_content or "").strip()


def format_section(record: Record, body: str) -> str:
    return (
        f"{DELIMITER}\n"
        "SOURCE START\n"
        f"File: {record.path}\n"
        f"Fingerprint: {record.fingerprint}\n"
        f"{DELIMITER}\n\n"
        f"{body.strip()}\n"
        f"{DELIMITER}\n"
        f"SOURCE END: {record.path}\n"
        f"{DELIMITER}\n"
    )


def convert_sources(source: Path, existing_fingerprints: set[str] | None = None, allow_duplicates: bool = False) -> tuple[list[Record], list[tuple[Record, str]]]:
    existing_fingerprints = existing_fingerprints or set()
    seen = set(existing_fingerprints)
    records: list[Record] = []
    sections: list[tuple[Record, str]] = []

    with tempfile.TemporaryDirectory() as tmp:
        files = gather_files(source, Path(tmp))
        for path in files:
            suffix = path.suffix.lower()
            data = path.read_bytes()
            rel = relative_to_source(path, source)

            if suffix in {".md", ".markdown"}:
                if path.name.startswith("prompt-"):
                    records.append(Record(path.name, rel, suffix, len(data), checksum_bytes(data), False, "skipped: project prompt file"))
                    continue
                text = data.decode("utf-8", errors="replace")
                if is_manifest_text(text):
                    records.append(Record(path.name, rel, suffix, len(data), checksum_bytes(data), False, "skipped: Markdown library manifest"))
                    continue
                if is_library_text(text):
                    imported = parse_sections(text)
                    if imported:
                        for sec in imported:
                            fp = sec.get("fingerprint") or checksum_text(sec["body"])
                            rec = Record(Path(sec["file"]).name, sec["file"], Path(sec["file"]).suffix.lower(), 0, fp, True, f"imported from Markdown library: {rel}")
                            if not allow_duplicates and fp in seen:
                                rec.included = False
                                rec.note = "not added: duplicate source fingerprint"
                                records.append(rec)
                                continue
                            seen.add(fp)
                            records.append(rec)
                            sections.append((rec, sec["raw"].rstrip() + "\n"))
                        continue

            fp = checksum_bytes(data)
            rec = Record(path.name, rel, suffix, len(data), fp, False)
            if suffix not in SUPPORTED_SUFFIXES:
                rec.note = "skipped: file type not supported"
                records.append(rec)
                continue
            if not allow_duplicates and fp in seen:
                rec.note = "not added: duplicate source fingerprint"
                records.append(rec)
                continue

            try:
                if suffix in {".txt", ".md", ".markdown", ".html", ".htm", ".csv"}:
                    body = read_plain(path)
                else:
                    body = convert_with_markitdown(path)
            except ImportError:
                rec.note = "skipped: this file type needs MarkItDown. Install with: python -m pip install 'markitdown[all]'"
                records.append(rec)
                continue
            except Exception as exc:
                rec.note = f"skipped: could not convert ({exc})"
                records.append(rec)
                continue
            if not body.strip():
                rec.note = "skipped: no readable text found"
                records.append(rec)
                continue
            rec.included = True
            records.append(rec)
            seen.add(fp)
            sections.append((rec, format_section(rec, body)))

    return records, sections


def manifest_header() -> str:
    return "| No. | File | Type | Size | Fingerprint | Status | Notes |\n|---:|---|---|---:|---|---|---|"


def manifest_row(rec: Record, no: int | str) -> str:
    status = "included" if rec.included else "skipped"
    return f"| {no} | {rec.path} | {rec.suffix or '(none)'} | {rec.size} | {rec.fingerprint} | {status} | {rec.note} |"


def write_library(output: Path, source: Path, records: list[Record], sections: list[str]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    included = [r for r in records if r.included]
    lines = [
        LIBRARY_MARKER,
        "# Markdown Library File",
        "",
        "This file was built by Make Markdown Library from your source files.",
        "Each source below is wrapped in START and END markers so an AI can tell the sources apart.",
        "",
        f"- Built on: {today}",
        f"- Source input: {source}",
        f"- Sources included: {len(included)}",
        f"- Sources skipped: {len(records) - len(included)}",
        "",
        "## Source manifest",
        "",
        manifest_header(),
    ]
    for i, rec in enumerate(included, start=1):
        lines.append(manifest_row(rec, i))
    lines += ["", "---", ""]
    output.write_text("\n".join(lines) + "\n" + "\n".join(sections), encoding="utf-8")
    write_manifest(output.with_name(output.stem + "-manifest.md"), source, records)


def write_library_from_sections(output: Path, sections: list[dict[str, str]], skipped: list[Record] | None = None) -> None:
    skipped = skipped or []
    records: list[Record] = []
    raw_sections: list[str] = []
    for sec in sections:
        rec = Record(Path(sec["file"]).name, sec["file"], Path(sec["file"]).suffix.lower(), 0, sec["fingerprint"], True)
        records.append(rec)
        raw_sections.append(sec["raw"].rstrip() + "\n")
    write_library(output, Path("updated library"), records + skipped, raw_sections)


def write_manifest(path: Path, source: Path, records: list[Record]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Markdown Library Manifest",
        "",
        f"Source input: {source}",
        "",
        manifest_header(),
    ]
    included_no = 0
    for rec in records:
        no: int | str
        if rec.included:
            included_no += 1
            no = included_no
        else:
            no = "-"
        lines.append(manifest_row(rec, no))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_sections(library: Path) -> list[dict[str, str]]:
    if not library.is_file():
        raise FileNotFoundError(f"Markdown library file not found: {library}")
    return parse_sections(library.read_text(encoding="utf-8"))


def command_setup(_args: argparse.Namespace) -> int:
    setup_project(Path.cwd())
    print("Markdown Mentor project folders are ready.")
    print("Put your source files in 1-source-files/.")
    print("Then run: python make-markdown-library.py make")
    return 0


def make_usage() -> str:
    return (
        "Correct use:\n"
        "  python make-markdown-library.py make\n"
        "  python make-markdown-library.py make SOURCE_FOLDER\n"
        "  python make-markdown-library.py make SOURCE_FOLDER DESTINATION_FOLDER\n"
        "  python make-markdown-library.py make SOURCE_FOLDER DESTINATION_FILE.md\n\n"
        "Examples:\n"
        "  python make-markdown-library.py make\n"
        "  python make-markdown-library.py make 1-source-files 2-markdown-library\n"
        "  python make-markdown-library.py make 1-source-files 2-markdown-library/markdown-library.md\n\n"
        "SOURCE_FOLDER is the folder containing your source files.\n"
        "DESTINATION_FOLDER is where the library should be saved. The tool will create markdown-library.md inside it.\n"
        "DESTINATION_FILE.md is the exact Markdown library file to write."
    )


def resolve_make_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    paths = [Path(p) for p in getattr(args, "paths", [])]
    if args.output and len(paths) > 1:
        raise SystemExit("Problem: use either DESTINATION_FOLDER/FILE or --output, not both.\n\n" + make_usage())
    if len(paths) > 2:
        raise SystemExit("Problem: too many paths were given to make.\n\n" + make_usage())

    source = paths[0] if paths else DEFAULT_SOURCE_DIR

    if args.output:
        output = Path(args.output)
    elif len(paths) == 2:
        destination = paths[1]
        if destination.suffix.lower() in {".md", ".markdown"}:
            output = destination
        else:
            output = destination / "markdown-library.md"
    else:
        output = DEFAULT_LIBRARY

    return source, output


def command_make(args: argparse.Namespace) -> int:
    source, output = resolve_make_paths(args)
    try:
        records, pairs = convert_sources(source, allow_duplicates=args.allow_duplicates)
        write_library(output, source, records, [section for _rec, section in pairs])
    except FileNotFoundError as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        print("", file=sys.stderr)
        print(make_usage(), file=sys.stderr)
        return 1
    print("Markdown library file made.")
    print(f"  Source:   {source}")
    print(f"  Library:  {output}")
    print(f"  Manifest: {output.with_name(output.stem + '-manifest.md')}")
    print(f"  Sources included: {sum(1 for r in records if r.included)}")
    print(f"  Sources skipped:  {sum(1 for r in records if not r.included)}")
    for rec in records:
        if rec.note.startswith("not added:"):
            print(f"  not added - {rec.path}")
    return 0


def command_add(args: argparse.Namespace) -> int:
    library = Path(args.library or DEFAULT_LIBRARY)
    source = Path(args.source)
    existing = read_sections(library)
    fingerprints = {s["fingerprint"] for s in existing if s.get("fingerprint")}
    records, pairs = convert_sources(source, existing_fingerprints=fingerprints, allow_duplicates=args.allow_duplicates)
    new_sections: list[dict[str, str]] = []
    for _rec, raw in pairs:
        new_sections.extend(parse_sections(raw))
    skipped = [r for r in records if r.note.startswith("not added:")]
    write_library_from_sections(library, existing + new_sections, skipped)
    print("Sources added to Markdown library file.")
    print(f"  Library:  {library}")
    print(f"  Sources added:   {len(new_sections)}")
    print(f"  Sources skipped: {len(records) - len(new_sections)}")
    for rec in skipped:
        print(f"  not added - {rec.path}")
    return 0


def command_list(args: argparse.Namespace) -> int:
    library = Path(args.library or DEFAULT_LIBRARY)
    sections = read_sections(library)
    if not sections:
        print("No sources found in this library file.")
        return 1
    print(f"Sources in {library}:")
    for i, sec in enumerate(sections, 1):
        print(f"  {i}. {sec['file']}")
    return 0


def command_remove(args: argparse.Namespace) -> int:
    if len(args.items) == 1:
        library = DEFAULT_LIBRARY
        selector = args.items[0]
    elif len(args.items) == 2:
        library = Path(args.items[0])
        selector = args.items[1]
    else:
        raise SystemExit("Use: remove-file 3  OR  remove-file path/to/markdown-library.md 3")
    sections = read_sections(library)
    if selector.isdigit():
        idx = int(selector)
        if idx < 1 or idx > len(sections):
            raise SystemExit(f"No source number {idx}. Run list first.")
        removed = sections.pop(idx - 1)
    else:
        matches = [s for s in sections if s["file"] == selector or Path(s["file"]).name == selector]
        if not matches:
            raise SystemExit(f"No source named {selector}. Run list first.")
        removed = matches[0]
        sections.remove(removed)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = library.with_name(f"{library.stem}-backup-{stamp}{library.suffix}")
    shutil.copy2(library, backup)
    write_library_from_sections(library, sections)
    print("Source removed from Markdown library file.")
    print(f"  Removed: {removed['file']}")
    print(f"  Backup:  {backup}")
    return 0


def command_check(args: argparse.Namespace) -> int:
    library = Path(args.library or DEFAULT_LIBRARY)
    sections = read_sections(library)
    text = library.read_text(encoding="utf-8")
    starts = len(re.findall(r"^SOURCE START$", text, flags=re.MULTILINE))
    ends = len(re.findall(r"^SOURCE END:", text, flags=re.MULTILINE))
    issues: list[str] = []
    if starts == 0:
        issues.append("No SOURCE START markers found.")
    if starts != ends:
        issues.append(f"Source markers do not match: {starts} starts, {ends} ends.")
    if starts != len(sections):
        issues.append("Some source sections could not be parsed.")
    print("Markdown library file check done.")
    print(f"  Sources: {len(sections)}")
    if issues:
        for issue in issues:
            print(f"  Problem: {issue}")
        return 1
    print("  The file has the expected source markers.")
    print("  This checks file structure only. It does not judge teaching fit.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Make and manage a Markdown library file.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup", help="Create the Markdown Mentor project folders in this folder.")
    p.set_defaults(func=command_setup)

    make_description = (
        "Make a new Markdown library file.\n\n"
        "Correct use:\n"
        "  python make-markdown-library.py make\n"
        "  python make-markdown-library.py make SOURCE_FOLDER\n"
        "  python make-markdown-library.py make SOURCE_FOLDER DESTINATION_FOLDER\n"
        "  python make-markdown-library.py make SOURCE_FOLDER DESTINATION_FILE.md\n\n"
        "Default: 1-source-files -> 2-markdown-library/markdown-library.md"
    )
    for name in ["make", "new"]:
        p = sub.add_parser(
            name,
            help="Make a new Markdown library file.",
            description=make_description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        p.add_argument("paths", nargs="*", metavar="path", help="Optional source folder and destination folder/file.")
        p.add_argument("-o", "--output", help="Output library file. Do not use this with a destination path.")
        p.add_argument("--allow-duplicates", action="store_true", help="Add duplicate source fingerprints instead of skipping them.")
        p.set_defaults(func=command_make)

    p = sub.add_parser("add", help="Add sources to the Markdown library file.")
    p.add_argument("source", help="Source file, folder, ZIP, or library to add.")
    p.add_argument("--library", help="Library file. Default: 2-markdown-library/markdown-library.md")
    p.add_argument("--allow-duplicates", action="store_true", help="Add duplicate source fingerprints instead of skipping them.")
    p.set_defaults(func=command_add)

    p = sub.add_parser("list", help="List sources in the Markdown library file.")
    p.add_argument("library", nargs="?", help="Library file. Default: 2-markdown-library/markdown-library.md")
    p.set_defaults(func=command_list)

    p = sub.add_parser("remove-file", help="Remove a source by list number or filename.")
    p.add_argument("items", nargs="+", help="Use: remove-file 3 OR remove-file library.md 3")
    p.set_defaults(func=command_remove)

    p = sub.add_parser("check-file", help="Check the Markdown library file structure.")
    p.add_argument("library", nargs="?", help="Library file. Default: 2-markdown-library/markdown-library.md")
    p.set_defaults(func=command_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
