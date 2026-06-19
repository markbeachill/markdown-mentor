"""Make Markdown library files.

Plain English: this turns a folder, ZIP, or source file into one tidy Markdown
file that an AI chatbot can read. Each source file becomes a clearly marked
section, so the AI can tell where one source ends and the next begins.

The user-facing command is `make-markdown-library`.

Who does what:
- The user collects the source files.
- The software converts them and writes the Markdown library file.
- The AI reads the library later, when you paste it into a chatbot.

This step needs MarkItDown, a free tool from Microsoft that converts Word,
PDF, PowerPoint, and other files into Markdown. If MarkItDown is not installed,
this code stops and tells you how to install it. There is no fallback on
purpose: the library file must be built the same way every time so the results
are reliable.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

# File types MarkItDown handles well and that make sense as source material.
SUPPORTED_SUFFIXES = {
    ".txt", ".md", ".markdown",
    ".docx", ".doc",
    ".pdf",
    ".pptx", ".ppt",
    ".html", ".htm",
    ".csv",
}

# A strong, unlikely-to-clash marker so the AI can see source boundaries.
DELIMITER = "=" * 70
LIBRARY_METADATA_MARKER = "<!-- markdown-library-file: true -->"


class MarkItDownMissing(RuntimeError):
    """Raised when MarkItDown is not installed.

    The message tells the user exactly what to do, in plain English.
    """


def _require_markitdown():
    """Load MarkItDown, or stop with a clear, friendly message."""
    try:
        from markitdown import MarkItDown  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised via message
        raise MarkItDownMissing(
            "This command needs MarkItDown to read your source files, "
            "and it is not installed yet.\n\n"
            "Command to copy:\n\n"
            "    pip install 'markitdown[all]'\n\n"
            "If that does not work, see docs/install-markitdown.md or the "
            "project website. MarkItDown is a free tool from Microsoft: "
            "https://github.com/microsoft/markitdown"
        ) from exc
    return MarkItDown()


@dataclass
class SourceRecord:
    """One entry in the source manifest.

    'Provenance' means a record of where the content came from. We keep the
    original file name, path, size, and a checksum (a short fingerprint of the
    file's contents) so the source can be traced later.
    """

    name: str
    relative_path: str
    suffix: str
    size_bytes: int
    checksum: str
    converted: bool
    note: str = ""


@dataclass
class BuildResult:
    """What the build or add command produced, so commands can report on it."""

    pack_path: Path
    manifest_path: Path
    records: list[SourceRecord] = field(default_factory=list)

    @property
    def converted_count(self) -> int:
        return sum(1 for r in self.records if r.converted)

    @property
    def skipped_count(self) -> int:
        return sum(1 for r in self.records if not r.converted)


@dataclass
class LibraryCheckReport:
    """A simple structural check of a Markdown library file."""

    library_path: Path
    source_count: int
    duplicate_count: int
    issues: list[str] = field(default_factory=list)

    @property
    def looks_valid(self) -> bool:
        return not self.issues


def _checksum(data: bytes) -> str:
    """Return a short fingerprint of file contents (first 12 hex characters)."""
    return hashlib.sha256(data).hexdigest()[:12]


def _safe_extract_zip(zip_path: Path, extract_to: Path) -> None:
    """Extract a ZIP without allowing paths to escape the target folder."""
    with zipfile.ZipFile(zip_path) as zf:
        root = extract_to.resolve()
        for member in zf.infolist():
            target = (extract_to / member.filename).resolve()
            if not str(target).startswith(str(root)):
                raise zipfile.BadZipFile("ZIP contains an unsafe file path")
        zf.extractall(extract_to)


def _gather_files(source_path: Path, work_dir: Path) -> list[Path]:
    """Find every usable file, unpacking ZIP files along the way.

    The input can be a single file, a folder, or a ZIP file. Nested ZIPs are
    handled: a ZIP inside a folder, and a ZIP inside a ZIP, are both expanded
    so their contents can be read.
    """
    found: list[Path] = []

    def handle_file(item: Path) -> None:
        if item.suffix.lower() == ".zip":
            extract_to = work_dir / (item.stem + "_unzipped")
            extract_to.mkdir(parents=True, exist_ok=True)
            try:
                _safe_extract_zip(item, extract_to)
            except zipfile.BadZipFile:
                # The caller will not get a converted record for a bad ZIP yet.
                # This keeps the current behaviour simple and non-fatal.
                return
            walk(extract_to)
        else:
            found.append(item)

    def walk(directory: Path) -> None:
        for item in sorted(directory.rglob("*")):
            if item.is_dir():
                continue
            handle_file(item)

    if source_path.is_dir():
        walk(source_path)
    elif source_path.is_file():
        handle_file(source_path)
    else:
        raise FileNotFoundError(f"Source not found: {source_path}")
    return found


def _relative_to_source(path: Path, source_path: Path) -> str:
    """Return a useful display path for the manifest and source marker."""
    try:
        base = source_path if source_path.is_dir() else source_path.parent
        return str(path.relative_to(base))
    except ValueError:
        return path.name


def _is_markdown_library_text(text: str) -> bool:
    """Return True if text looks like a Markdown library file.

    New library files include LIBRARY_METADATA_MARKER. Older library files are
    still accepted if they contain balanced source markers. This lets users put
    an older Markdown library into the source folder and have its sources
    imported as separate sources.
    """
    if LIBRARY_METADATA_MARKER in text:
        return True
    return "SOURCE START" in text and "SOURCE END:" in text and "Fingerprint:" in text


def _is_markdown_library_manifest_text(text: str) -> bool:
    """Return True if a Markdown file looks like a library manifest."""
    return "# Markdown Library Manifest" in text and "| No. | File |" in text


def _record_from_imported_section(section: dict[str, str], library_path: Path, source_path: Path) -> SourceRecord:
    """Create a source record for a section imported from another library file."""
    file_name = section["file"]
    return SourceRecord(
        name=Path(file_name).name,
        relative_path=file_name,
        suffix=Path(file_name).suffix.lower(),
        size_bytes=0,
        checksum=section.get("fingerprint", ""),
        converted=True,
        note=f"imported from Markdown library: {_relative_to_source(library_path, source_path)}",
    )


def _dedupe_section_pairs(
    records: list[SourceRecord],
    section_pairs: list[tuple[SourceRecord, str]],
    *,
    existing_fingerprints: set[str] | None = None,
    allow_duplicates: bool = False,
) -> list[tuple[SourceRecord, str]]:
    """Remove duplicate sections unless the user has explicitly allowed them.

    Duplicates are identified by source fingerprint. When a duplicate is not
    added, the record stays in the manifest with a clear note. The CLI also
    prints "not added - filename" for each duplicate.
    """
    if allow_duplicates:
        return section_pairs

    seen = set(existing_fingerprints or set())
    kept: list[tuple[SourceRecord, str]] = []
    for record, section in section_pairs:
        if record.checksum and record.checksum in seen:
            record.converted = False
            record.note = "not added: duplicate source fingerprint"
            continue
        if record.checksum:
            seen.add(record.checksum)
        kept.append((record, section))
    return kept


def _convert_sources(
    source_path: Path,
    *,
    existing_fingerprints: set[str] | None = None,
    allow_duplicates: bool = False,
) -> tuple[list[SourceRecord], list[tuple[SourceRecord, str]]]:
    """Convert source files and return records plus source sections.

    If the source input contains an existing Markdown library file, the tool
    imports each source section from that library as a separate source. It does
    not wrap the whole library as one file. This keeps the new library readable
    to AI as a set of separate files.
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        files = _gather_files(source_path, work_dir)

        records: list[SourceRecord] = []
        section_pairs: list[tuple[SourceRecord, str]] = []
        md = None

        for path in files:
            data = path.read_bytes()
            suffix = path.suffix.lower()

            if suffix in {".md", ".markdown"}:
                try:
                    text = data.decode("utf-8")
                except UnicodeDecodeError:
                    text = data.decode("utf-8", errors="replace")

                if _is_markdown_library_text(text):
                    imported_sections = _parse_library_sections(text)
                    if imported_sections:
                        for section in imported_sections:
                            record = _record_from_imported_section(section, path, source_path)
                            records.append(record)
                            section_pairs.append((record, section["raw"]))
                        continue

                if _is_markdown_library_manifest_text(text):
                    records.append(SourceRecord(
                        name=path.name,
                        relative_path=_relative_to_source(path, source_path),
                        suffix=suffix,
                        size_bytes=len(data),
                        checksum=_checksum(data),
                        converted=False,
                        note="skipped: Markdown library manifest",
                    ))
                    continue

            record = SourceRecord(
                name=path.name,
                relative_path=_relative_to_source(path, source_path),
                suffix=suffix,
                size_bytes=len(data),
                checksum=_checksum(data),
                converted=False,
            )

            if suffix not in SUPPORTED_SUFFIXES:
                record.note = "skipped: file type not supported"
                records.append(record)
                continue

            try:
                if md is None:
                    md = _require_markitdown()
                result = md.convert(str(path))
                text = (result.text_content or "").strip()
            except Exception as exc:  # noqa: BLE001 - report, do not crash
                record.note = f"skipped: could not convert ({exc})"
                records.append(record)
                continue

            if not text:
                record.note = "skipped: no readable text found"
                records.append(record)
                continue

            record.converted = True
            records.append(record)
            section_pairs.append((record, _format_section(record, text)))

    section_pairs = _dedupe_section_pairs(
        records,
        section_pairs,
        existing_fingerprints=existing_fingerprints,
        allow_duplicates=allow_duplicates,
    )
    return records, section_pairs


def build_library(
    source_path: str | Path,
    output_path: str | Path | None = None,
    purpose: str = "",
    *,
    title: str = "Markdown Library File",
    maker_name: str = "Make Markdown Library",
    allow_duplicates: bool = False,
) -> BuildResult:
    """Build a Markdown library file from a file, folder, or ZIP.

    Arguments:
        source_path: a source file, folder, or ZIP file. Folders may contain
            sub-folders and ZIP files.
        output_path: where to write the Markdown library file. Defaults to
            'markdown-library.md' next to the source folder or file.
        purpose: an optional one-line note recorded at the top of the library.
        title: the heading to use for the file.
        maker_name: the public name of the tool that built the file.
    """
    source_path = Path(source_path).expanduser().resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source_path}")

    if output_path is None:
        parent = source_path.parent if source_path.is_file() else source_path.parent
        output_path = parent / "markdown-library.md"
    output_path = Path(output_path).expanduser().resolve()
    manifest_path = output_path.with_name(output_path.stem + "-manifest.md")

    records, section_pairs = _convert_sources(source_path, allow_duplicates=allow_duplicates)
    sections = [section for _, section in section_pairs]

    _write_library(output_path, purpose, source_path, records, sections, title, maker_name)
    _write_manifest(manifest_path, purpose, source_path, records)

    return BuildResult(pack_path=output_path, manifest_path=manifest_path, records=records)



def add_to_library(
    library_path: str | Path,
    source_path: str | Path,
    purpose: str = "",
    *,
    skip_duplicates: bool = True,
) -> BuildResult:
    """Add more source files to an existing Markdown library file."""
    library_path = Path(library_path).expanduser().resolve()
    source_path = Path(source_path).expanduser().resolve()

    if not library_path.is_file():
        raise FileNotFoundError(f"Markdown library file not found: {library_path}")
    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source_path}")

    existing_text = library_path.read_text(encoding="utf-8")
    existing_sections = _parse_library_sections(existing_text)
    existing_fingerprints = {sec.get("fingerprint", "") for sec in existing_sections}
    manifest_path = library_path.with_name(library_path.stem + "-manifest.md")

    records, section_pairs = _convert_sources(
        source_path,
        existing_fingerprints=existing_fingerprints,
        allow_duplicates=not skip_duplicates,
    )
    sections_to_add = [section for _, section in section_pairs]

    if sections_to_add:
        new_sections: list[dict[str, str]] = []
        for section in sections_to_add:
            new_sections.extend(_parse_library_sections(section))
        all_sections = existing_sections + new_sections
        _write_library_from_sections(library_path, all_sections)
        not_added = [r for r in records if r.note.startswith("not added:")]
        _write_manifest_from_sections(manifest_path, all_sections, not_added)
    else:
        _append_manifest(manifest_path, purpose, source_path, records)

    return BuildResult(pack_path=library_path, manifest_path=manifest_path, records=records)


def list_library_sources(library_path: str | Path) -> list[str]:
    """Return the source names recorded in a Markdown library file."""
    library_path = Path(library_path).expanduser().resolve()
    if not library_path.is_file():
        raise FileNotFoundError(f"Markdown library file not found: {library_path}")
    text = library_path.read_text(encoding="utf-8")
    return re.findall(r"^File: (.+)$", text, flags=re.MULTILINE)


def check_library_format(library_path: str | Path) -> LibraryCheckReport:
    """Check whether a file looks like a valid Markdown library file."""
    library_path = Path(library_path).expanduser().resolve()
    if not library_path.is_file():
        raise FileNotFoundError(f"Markdown library file not found: {library_path}")
    text = library_path.read_text(encoding="utf-8")
    starts = len(re.findall(r"^SOURCE START$", text, flags=re.MULTILINE))
    ends = len(re.findall(r"^SOURCE END:", text, flags=re.MULTILINE))
    fingerprints = re.findall(r"Fingerprint: (\w+)", text)
    duplicate_count = len(fingerprints) - len(set(fingerprints))
    issues: list[str] = []
    if starts == 0:
        issues.append("No SOURCE START markers found.")
    if starts != ends:
        issues.append(f"Source markers do not match: {starts} starts, {ends} ends.")
    if starts != len(fingerprints):
        issues.append("Some source sections may be missing fingerprints.")
    return LibraryCheckReport(
        library_path=library_path,
        source_count=starts,
        duplicate_count=duplicate_count,
        issues=issues,
    )


def _format_section(record: SourceRecord, text: str) -> str:
    """Wrap one converted source in clear start and end markers."""
    header = (
        f"{DELIMITER}\n"
        f"SOURCE START\n"
        f"File: {record.relative_path}\n"
        f"Fingerprint: {record.checksum}\n"
        f"{DELIMITER}\n"
    )
    footer = f"\n{DELIMITER}\nSOURCE END: {record.relative_path}\n{DELIMITER}\n"
    return f"{header}\n{text}\n{footer}"



def _write_library(
    output_path: Path,
    purpose: str,
    source_path: Path,
    records: list[SourceRecord],
    sections: list[str],
    title: str,
    maker_name: str,
) -> None:
    today = _dt.date.today().isoformat()
    converted = [r for r in records if r.converted]
    lines = [
        LIBRARY_METADATA_MARKER,
        f"# {title}",
        "",
        f"This file was built by {maker_name} from your source files.",
        "It is a structured Markdown library that an AI chatbot can read. "
        "Each source below is wrapped in START and END markers so the AI can "
        "tell the sources apart.",
        "",
        f"- Built on: {today}",
        f"- Source input: {source_path.name}",
        f"- Sources included: {len(converted)}",
        f"- Sources skipped: {len(records) - len(converted)}",
    ]
    if purpose:
        lines += ["", f"**Purpose:** {purpose}"]
    lines += ["", "## Source manifest", "", _manifest_table_header()]
    for i, r in enumerate(converted, start=1):
        lines.append(_manifest_row(r, i))
    lines += ["", "---", ""]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n" + "\n".join(sections), encoding="utf-8")


def _write_library_from_sections(output_path: Path, sections: list[dict[str, str]]) -> None:
    """Rewrite a library file from parsed source sections, with a fresh manifest."""
    today = _dt.date.today().isoformat()
    lines = [
        LIBRARY_METADATA_MARKER,
        "# Markdown Library File",
        "",
        "This file was built by Make Markdown Library from your source files.",
        "It is a structured Markdown library that an AI chatbot can read. Each source below is wrapped in START and END markers so the AI can tell the sources apart.",
        "",
        f"- Updated on: {today}",
        f"- Sources included: {len(sections)}",
        "",
        "## Source manifest",
        "",
        _manifest_table_header(),
    ]
    for i, sec in enumerate(sections, start=1):
        record = SourceRecord(
            name=Path(sec["file"]).name,
            relative_path=sec["file"],
            suffix=Path(sec["file"]).suffix.lower(),
            size_bytes=0,
            checksum=sec.get("fingerprint", ""),
            converted=True,
        )
        lines.append(_manifest_row(record, i))
    lines += ["", "---", ""]
    output_path.write_text("\n".join(lines) + "\n" + "\n".join(sec["raw"].rstrip() for sec in sections) + "\n", encoding="utf-8")


def _write_manifest(
    manifest_path: Path,
    purpose: str,
    source_path: Path,
    records: list[SourceRecord],
) -> None:
    """Write a human-readable list of every file we looked at."""
    lines = [
        "# Markdown Library Manifest",
        "",
        "This is a plain list of every file the tool found, and what happened to it.",
        "",
        f"- Source input: {source_path}",
    ]
    if purpose:
        lines += [f"- Purpose: {purpose}"]
    lines += ["", _manifest_table_header()]
    for i, r in enumerate(records, start=1):
        lines.append(_manifest_row(r, i))
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_manifest_from_sections(
    manifest_path: Path,
    sections: list[dict[str, str]],
    not_added_records: list[SourceRecord] | None = None,
) -> None:
    """Write a manifest from the source sections currently in a library file."""
    lines = [
        "# Markdown Library Manifest",
        "",
        "This manifest was regenerated from the current Markdown library file.",
        "",
        _manifest_table_header(),
    ]
    for i, sec in enumerate(sections, start=1):
        record = SourceRecord(
            name=Path(sec["file"]).name,
            relative_path=sec["file"],
            suffix=Path(sec["file"]).suffix.lower(),
            size_bytes=0,
            checksum=sec.get("fingerprint", ""),
            converted=True,
        )
        lines.append(_manifest_row(record, i))
    if not_added_records:
        lines += ["", "## Files not added in the last run", "", _manifest_table_header()]
        start = len(sections) + 1
        for i, record in enumerate(not_added_records, start=start):
            lines.append(_manifest_row(record, i))
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _append_manifest(
    manifest_path: Path,
    purpose: str,
    source_path: Path,
    records: list[SourceRecord],
) -> None:
    """Add a run section to a source manifest next to the library file."""
    today = _dt.date.today().isoformat()
    if manifest_path.exists():
        prefix = manifest_path.read_text(encoding="utf-8")
        lines = [prefix.rstrip(), "", "---", "", f"## Sources added on {today}", ""]
    else:
        lines = ["# Markdown Library Manifest", "", f"## Sources added on {today}", ""]
    lines += [f"- Source input: {source_path}"]
    if purpose:
        lines += [f"- Purpose: {purpose}"]
    lines += ["", _manifest_table_header()]
    start = _manifest_source_count(manifest_path) + 1 if manifest_path.exists() else 1
    for i, r in enumerate(records, start=start):
        lines.append(_manifest_row(r, i))
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _manifest_source_count(manifest_path: Path) -> int:
    if not manifest_path.exists():
        return 0
    return len(re.findall(r"^\|\s*\d+\s*\|", manifest_path.read_text(encoding="utf-8"), flags=re.MULTILINE))


def _manifest_table_header() -> str:
    return "| No. | File | Type | Size (bytes) | Fingerprint | Status |\n| ---: | --- | --- | ---: | --- | --- |"


def _manifest_row(record: SourceRecord, number: int) -> str:
    status = "included" if record.converted else (record.note or "skipped")
    size = record.size_bytes if record.size_bytes else ""
    return (
        f"| {number} | {record.relative_path} | {record.suffix or ''} | "
        f"{size} | {record.checksum} | {status} |"
    )


def _parse_library_sections(text: str) -> list[dict[str, str]]:
    """Return source sections from a Markdown library file."""
    pattern = re.compile(
        rf"{re.escape(DELIMITER)}\nSOURCE START\nFile: (?P<file>.*?)\nFingerprint: (?P<fingerprint>.*?)\n{re.escape(DELIMITER)}\n(?P<body>.*?)\n{re.escape(DELIMITER)}\nSOURCE END: .*?\n{re.escape(DELIMITER)}",
        flags=re.DOTALL,
    )
    sections: list[dict[str, str]] = []
    for match in pattern.finditer(text):
        sections.append({
            "file": match.group("file").strip(),
            "fingerprint": match.group("fingerprint").strip(),
            "raw": match.group(0),
        })
    return sections


def remove_file_from_library(library_path: str | Path, selector: str | int) -> BuildResult:
    """Remove one source section from a Markdown library by number or filename.

    The number is the one printed by `make-markdown-library list`.
    """
    library_path = Path(library_path).expanduser().resolve()
    if not library_path.is_file():
        raise FileNotFoundError(f"Markdown library file not found: {library_path}")

    text = library_path.read_text(encoding="utf-8")
    sections = _parse_library_sections(text)
    if not sections:
        raise ValueError("No source sections were found in this Markdown library file.")

    index: int | None = None
    selector_text = str(selector).strip()
    if selector_text.isdigit():
        number = int(selector_text)
        if number < 1 or number > len(sections):
            raise ValueError(f"Source number {number} is out of range. Use `make-markdown-library list` to see the numbers.")
        index = number - 1
    else:
        matches = [i for i, sec in enumerate(sections) if sec["file"] == selector_text or Path(sec["file"]).name == selector_text]
        if not matches:
            raise ValueError(f"No source named {selector_text!r} was found. Use `make-markdown-library list` to see names.")
        if len(matches) > 1:
            raise ValueError(f"More than one source matched {selector_text!r}. Remove by number instead.")
        index = matches[0]

    removed = sections.pop(index)
    backup_path = library_path.with_name(library_path.stem + ".backup.md")
    backup_path.write_text(text, encoding="utf-8")

    _write_library_from_sections(library_path, sections)
    manifest_path = library_path.with_name(library_path.stem + "-manifest.md")
    _write_manifest_from_sections(manifest_path, sections)

    record = SourceRecord(
        name=Path(removed["file"]).name,
        relative_path=removed["file"],
        suffix=Path(removed["file"]).suffix.lower(),
        size_bytes=0,
        checksum=removed.get("fingerprint", ""),
        converted=True,
        note="removed",
    )
    return BuildResult(pack_path=library_path, manifest_path=manifest_path, records=[record])
