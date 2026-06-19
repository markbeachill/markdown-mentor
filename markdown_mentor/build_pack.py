"""Make Markdown library files and teaching content packs.

Plain English: this turns a folder, ZIP, or source file into one tidy Markdown
file that an AI chatbot can read. Each source file becomes a clearly marked
section, so the AI can tell where one source ends and the next begins.

There are two user-facing names for this idea:

- Markdown Library Maker makes a general Markdown library file.
- Markdown Mentor uses the same file as a teaching content pack.

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


def _convert_sources(source_path: Path) -> tuple[list[SourceRecord], list[tuple[SourceRecord, str]]]:
    """Convert source files and return records plus source sections."""
    md = _require_markitdown()

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        files = _gather_files(source_path, work_dir)

        records: list[SourceRecord] = []
        sections: list[tuple[SourceRecord, str]] = []

        for path in files:
            data = path.read_bytes()
            suffix = path.suffix.lower()
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
            sections.append((record, _format_section(record, text)))

    return records, sections


def build_library(
    source_path: str | Path,
    output_path: str | Path | None = None,
    purpose: str = "",
    *,
    title: str = "Markdown Library File",
    maker_name: str = "Markdown Library Maker",
) -> BuildResult:
    """Build a Markdown library file from a file, folder, or ZIP.

    Arguments:
        source_path: a source file, folder, or ZIP file. Folders may contain
            sub-folders and ZIP files.
        output_path: where to write the Markdown library file. Defaults to
            'markdown-library.md' next to the source folder or file.
        purpose: an optional one-line note recorded at the top of the library.
        title: the heading to use for the file. Markdown Mentor uses this to
            keep the education-facing name 'Educational Content Training Pack'.
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

    records, section_pairs = _convert_sources(source_path)
    sections = [section for _, section in section_pairs]

    _write_library(output_path, purpose, source_path, records, sections, title, maker_name)
    _write_manifest(manifest_path, purpose, source_path, records)

    return BuildResult(pack_path=output_path, manifest_path=manifest_path, records=records)


def build_pack(
    source_dir: str | Path,
    output_path: str | Path | None = None,
    goal: str = "",
) -> BuildResult:
    """Build a teaching content pack from a folder of source files.

    This is the education-facing alias used by Markdown Mentor. The underlying
    file format is the same as a Markdown library file.
    """
    source_path = Path(source_dir).expanduser().resolve()
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source folder not found: {source_path}")
    if output_path is None:
        output_path = source_path.parent / "content-pack.md"
    return build_library(
        source_path,
        output_path,
        goal,
        title="Educational Content Training Pack",
        maker_name="Markdown Mentor",
    )


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
    existing_fingerprints = set(re.findall(r"Fingerprint: (\w+)", existing_text))
    manifest_path = library_path.with_name(library_path.stem + "-manifest.md")

    records, section_pairs = _convert_sources(source_path)
    sections_to_add: list[str] = []

    for record, section in section_pairs:
        if skip_duplicates and record.checksum in existing_fingerprints:
            record.converted = False
            record.note = "skipped: duplicate already in library"
            continue
        sections_to_add.append(section)

    if sections_to_add:
        today = _dt.date.today().isoformat()
        note = [
            "",
            "---",
            "",
            f"## Sources added on {today}",
            "",
        ]
        if purpose:
            note += [f"Purpose: {purpose}", ""]
        with library_path.open("a", encoding="utf-8") as fh:
            if existing_text and not existing_text.endswith("\n"):
                fh.write("\n")
            fh.write("\n".join(note))
            fh.write("\n".join(sections_to_add))
            fh.write("\n")

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
    lines += ["", "---", ""]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n" + "\n".join(sections), encoding="utf-8")


def _write_manifest(
    manifest_path: Path,
    purpose: str,
    source_path: Path,
    records: list[SourceRecord],
) -> None:
    """Write a human-readable list of every file we looked at."""
    lines = [
        "# Source Manifest",
        "",
        "This is a plain list of every file the tool found, and what happened to it.",
        "",
        f"- Source input: {source_path}",
    ]
    if purpose:
        lines += [f"- Purpose: {purpose}"]
    lines += ["", _manifest_table_header()]
    for r in records:
        lines.append(_manifest_row(r))
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
        lines = ["# Source Manifest", "", f"## Sources added on {today}", ""]
    lines += [f"- Source input: {source_path}"]
    if purpose:
        lines += [f"- Purpose: {purpose}"]
    lines += ["", _manifest_table_header()]
    for r in records:
        lines.append(_manifest_row(r))
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _manifest_table_header() -> str:
    return "| File | Type | Size (bytes) | Fingerprint | Status |\n| --- | --- | --- | --- | --- |"


def _manifest_row(record: SourceRecord) -> str:
    status = "included" if record.converted else (record.note or "skipped")
    return (
        f"| {record.relative_path} | {record.suffix or '(none)'} | "
        f"{record.size_bytes} | {record.checksum} | {status} |"
    )
