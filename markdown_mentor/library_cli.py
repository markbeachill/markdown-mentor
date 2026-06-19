"""Command line for Make Markdown Library.

This is the general-purpose half of the project. It makes one structured
Markdown library file from many source files, or adds more sources to an
existing library file.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .build_pack import (
    MarkItDownMissing,
    add_to_library,
    build_library,
    check_library_format,
    list_library_sources,
    remove_file_from_library,
)


def _print_not_added(result) -> None:
    for record in result.records:
        if record.note.startswith("not added:"):
            print(f"  not added - {record.relative_path}")


def _cmd_make(args: argparse.Namespace) -> int:
    try:
        result = build_library(
            args.source,
            args.output,
            args.purpose or "",
            allow_duplicates=args.allow_duplicates,
        )
    except MarkItDownMissing as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    print("Markdown library file made.")
    print(f"  Library:  {result.pack_path}")
    print(f"  Manifest: {result.manifest_path}")
    print(f"  Sources included: {result.converted_count}")
    print(f"  Sources skipped:  {result.skipped_count}")
    if result.skipped_count:
        _print_not_added(result)
        print("  Read the manifest to see why some files were skipped.")
    return 0


def _cmd_add(args: argparse.Namespace) -> int:
    try:
        result = add_to_library(
            args.library,
            args.source,
            args.purpose or "",
            skip_duplicates=not args.allow_duplicates,
        )
    except MarkItDownMissing as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    print("Sources added to Markdown library file.")
    print(f"  Library:  {result.pack_path}")
    print(f"  Manifest: {result.manifest_path}")
    print(f"  Sources added:   {result.converted_count}")
    print(f"  Sources skipped: {result.skipped_count}")
    if result.skipped_count:
        _print_not_added(result)
        print("  Read the manifest to see why some files were skipped.")
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    try:
        sources = list_library_sources(args.library)
    except FileNotFoundError as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    if not sources:
        print("No sources found in this library file.")
        return 1
    print(f"Sources in {args.library}:")
    for idx, source in enumerate(sources, start=1):
        print(f"  {idx}. {source}")
    return 0



def _cmd_remove_file(args: argparse.Namespace) -> int:
    try:
        result = remove_file_from_library(args.library, args.selector)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    removed = result.records[0].relative_path if result.records else args.selector
    print("Source removed from Markdown library file.")
    print(f"  Removed:  {removed}")
    print(f"  Library:  {result.pack_path}")
    print(f"  Manifest: {result.manifest_path}")
    print("  A backup was saved next to the library file.")
    return 0

def _cmd_check(args: argparse.Namespace) -> int:
    try:
        report = check_library_format(args.library)
    except FileNotFoundError as exc:
        print(f"Problem: {exc}", file=sys.stderr)
        return 1

    print("Markdown library file check done.")
    print(f"  Sources: {report.source_count}")
    print(f"  Duplicate fingerprints: {report.duplicate_count}")
    if report.issues:
        print("  Problems found:")
        for issue in report.issues:
            print(f"  - {issue}")
        return 1
    print("  The file has the expected source markers.")
    print("  This only checks the file structure. It does not judge whether the sources fit a teaching approach.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="make-markdown-library",
        description="Make one structured Markdown library file from source files.",
    )
    parser.add_argument("--version", action="version", version=f"make-markdown-library {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_make = sub.add_parser(
        "new",
        help="Make a new Markdown library file from a file, folder, or ZIP.",
    )
    p_make.add_argument("source", help="A source file, folder, ZIP file, or existing Markdown library file.")
    p_make.add_argument("-o", "--output", help="Where to save the Markdown library file.")
    p_make.add_argument("-p", "--purpose", help="A short note about what this library is for.")
    p_make.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Add sources even when the same fingerprint appears more than once.",
    )
    p_make.set_defaults(func=_cmd_make)

    p_add = sub.add_parser(
        "add",
        help="Add source files to an existing Markdown library file.",
    )
    p_add.add_argument("library", help="The existing Markdown library file.")
    p_add.add_argument("source", help="A new source file, folder, ZIP file, or existing Markdown library file to add.")
    p_add.add_argument("-p", "--purpose", help="A short note about why you are adding these sources.")
    p_add.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Add sources even when their fingerprints are already in the library.",
    )
    p_add.set_defaults(func=_cmd_add)

    p_list = sub.add_parser(
        "list",
        help="List the sources recorded in a Markdown library file.",
    )
    p_list.add_argument("library", help="The Markdown library file to inspect.")
    p_list.set_defaults(func=_cmd_list)


    p_remove = sub.add_parser(
        "remove-file",
        help="Remove one source from a Markdown library file by list number or filename.",
    )
    p_remove.add_argument("library", help="The Markdown library file to edit.")
    p_remove.add_argument("selector", help="The source number from `list`, or the filename to remove.")
    p_remove.set_defaults(func=_cmd_remove_file)

    p_check = sub.add_parser(
        "check-file",
        help="Check that a Markdown library file has the expected source markers.",
    )
    p_check.add_argument("library", help="The Markdown library file to check.")
    p_check.set_defaults(func=_cmd_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
