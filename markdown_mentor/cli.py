"""The Markdown Mentor command line.

Markdown Mentor is the education workflow. It helps you use a Markdown library
file to plan, draft, and export teaching materials.

The general file-making tool is separate:

    make-markdown-library new <file-folder-or-zip>
    make-markdown-library add <library.md> <new-file-folder-or-zip>

Markdown Mentor does not judge source quality in Python. Teaching checks are AI
prompt steps that the teacher reviews.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .guide import run_guide
from .project import new_project

VALID_FORMATS = {"docx", "pptx", "html", "pdf"}


def _cmd_new_project(args: argparse.Namespace) -> int:
    try:
        result = new_project(args.folder, overwrite=args.overwrite)
    except FileExistsError as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    print("Markdown Mentor project folder made.")
    print(f"  Project folder: {result.path}")
    print("  Put source files in: 1-source-files/")
    print("  First command to run from inside the project folder:")
    print("    make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md")
    print("  Then upload 2-markdown-library/markdown-library.md to AI and use 3-teaching-approach/prompt-create-teaching-approach.md")
    if result.skipped:
        print(f"  Existing files left unchanged: {len(result.skipped)}")
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    try:
        from .export import LibreOfficeMissing, export_path
        result = export_path(args.input, args.format, args.output_dir, args.style)
    except LibreOfficeMissing as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    if not result.outputs:
        print("No Markdown (.md) files were found to convert.")
        return 1

    print(f"Converted {len(result.outputs)} file(s) to {args.format.upper()}:")
    for src, dst in zip(result.inputs, result.outputs):
        print(f"  {src.name}  ->  {dst}")
    return 0


def _cmd_guide(args: argparse.Namespace) -> int:
    return run_guide(args.project)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="markdown-mentor",
        description="Create a project folder, then use a Markdown library file to plan, draft, and export teaching materials.",
    )
    parser.add_argument("--version", action="version", version=f"markdown-mentor {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser(
        "new-project",
        help="Make a numbered project folder for a teaching-material project.",
    )
    p_new.add_argument("folder", help="Name or path of the project folder to create.")
    p_new.add_argument("--overwrite", action="store_true", help="Replace starter files if they already exist.")
    p_new.set_defaults(func=_cmd_new_project)

    p_guide = sub.add_parser(
        "guide",
        help="Show the teaching workflow step by step.",
    )
    p_guide.add_argument("project", nargs="?", help="Your project folder, or a Markdown library file (optional).")
    p_guide.set_defaults(func=_cmd_guide)

    p_export = sub.add_parser(
        "export",
        help="Turn Markdown teaching materials into Word, PowerPoint, web, or PDF files.",
    )
    p_export.add_argument("input", help="A Markdown file, or a folder of Markdown files.")
    p_export.add_argument(
        "-f", "--format", required=True, choices=sorted(VALID_FORMATS),
        help="The format to produce: docx, pptx, html, or pdf (pdf needs LibreOffice).",
    )
    p_export.add_argument("-o", "--output-dir", help="Folder to save the converted files in.")
    p_export.add_argument("-s", "--style", help="A Markdown style file. In a project folder this is usually style/style.md.")
    p_export.set_defaults(func=_cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
