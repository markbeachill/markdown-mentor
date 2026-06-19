"""The Markdown Mentor command line.

Plain English: this is what you type in a terminal to use the tool. There are
three commands:

    markdown-mentor build-pack <folder>     build a content pack from a folder
    markdown-mentor check-pack <pack.md>    check whether a pack is ready
    markdown-mentor export <file-or-folder> turn Markdown into Word/slides/web

Run any command with --help to see its options. Every command prints what it
did and where it saved the result, so you are never left guessing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .build_pack import build_pack, MarkItDownMissing
from .check_pack import check_pack
from .export import export_path, VALID_FORMATS, LibreOfficeMissing
from .guide import run_guide


def _cmd_build_pack(args: argparse.Namespace) -> int:
    try:
        result = build_pack(args.folder, args.output, args.goal or "")
    except MarkItDownMissing as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (NotADirectoryError, FileNotFoundError) as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    print("Content pack built.")
    print(f"  Pack:     {result.pack_path}")
    print(f"  Manifest: {result.manifest_path}")
    print(f"  Sources included: {result.converted_count}")
    print(f"  Sources skipped:  {result.skipped_count}")
    if result.skipped_count:
        print("  (See the manifest for why some files were skipped.)")
    print("\nNext step: check the pack with")
    print(f"  markdown-mentor check-pack \"{result.pack_path}\"")
    return 0


def _cmd_check_pack(args: argparse.Namespace) -> int:
    try:
        report = check_pack(args.pack, args.goal or "")
    except FileNotFoundError as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    print("Readiness check done.")
    print(f"  Sources: {report.source_count}    Words: {report.word_count}")
    print(f"  Risks: {report.risk_count}    Worth checking: {report.watch_count}")
    print(f"  Full note saved to: {report.note_path}")
    if report.risk_count:
        print("\nThere are risks worth fixing before you continue:")
        for f in report.findings:
            if f.level == "risk":
                print(f"  - {f.message}")
    else:
        print("\nNo blocking problems found. Read the note for things worth checking.")
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    try:
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


def _cmd_start(args: argparse.Namespace) -> int:
    return run_guide(args.folder)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="markdown-mentor",
        description="Turn teaching files into teaching materials, with the help of AI.",
    )
    parser.add_argument("--version", action="version", version=f"markdown-mentor {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser(
        "start",
        help="Walk through the whole workflow step by step (recommended first).",
    )
    p_start.add_argument("folder", nargs="?", help="Folder with your source files (optional).")
    p_start.set_defaults(func=_cmd_start)

    p_build = sub.add_parser(
        "build-pack",
        help="Build a content pack from a folder of source files.",
    )
    p_build.add_argument("folder", help="Folder containing your source files.")
    p_build.add_argument("-o", "--output", help="Where to save the content pack (.md).")
    p_build.add_argument("-g", "--goal", help="A one-line teaching goal to record in the pack.")
    p_build.set_defaults(func=_cmd_build_pack)

    p_check = sub.add_parser(
        "check-pack",
        help="Check whether a content pack is ready to teach from.",
    )
    p_check.add_argument("pack", help="The content pack Markdown file to check.")
    p_check.add_argument("-g", "--goal", help="The teaching goal, for context.")
    p_check.set_defaults(func=_cmd_check_pack)

    p_export = sub.add_parser(
        "export",
        help="Turn Markdown teaching materials into Word, PowerPoint, or web files.",
    )
    p_export.add_argument("input", help="A Markdown file, or a folder of Markdown files.")
    p_export.add_argument(
        "-f", "--format", required=True, choices=sorted(VALID_FORMATS),
        help="The format to produce: docx, pptx, html, or pdf (pdf needs LibreOffice).",
    )
    p_export.add_argument("-o", "--output-dir", help="Folder to save the converted files in.")
    p_export.add_argument("-s", "--style", help="A style profile (JSON) file.")
    p_export.set_defaults(func=_cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
