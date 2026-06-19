"""Build the Educational Content Training Pack (ECTP).

Plain English: this turns a folder of teaching files into one tidy Markdown
file that an AI chatbot can read. Each source file becomes a clearly marked
section, so the AI can tell where one source ends and the next begins.

Who does what:
- The user collects the source files into a folder.
- Markdown Mentor (this code) converts them and writes the content pack.
- The AI reads the content pack later, when you paste it into a chatbot.

This step needs MarkItDown, a free tool from Microsoft that converts Word,
PDF, PowerPoint, and other files into Markdown. If MarkItDown is not installed,
this code stops and tells you how to install it. There is no fallback on
purpose: the content pack must be built the same way every time so the results
are reliable.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

# File types MarkItDown handles well and that make sense as teaching sources.
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
            "Markdown Mentor needs MarkItDown to read your source files, "
            "and it is not installed yet.\n\n"
            "To install it, open a terminal and run:\n\n"
            "    pip install 'markitdown[all]'\n\n"
            "If that does not work, see the install guide at "
            "docs/install-markitdown.md or the project website. "
            "MarkItDown is a free tool from Microsoft: "
            "https://github.com/microsoft/markitdown"
        ) from exc
    return MarkItDown()


@dataclass
class SourceRecord:
    """One entry in the source manifest.

    'provenance' means a record of where the content came from. We keep the
    original file name, its size, and a checksum (a short fingerprint of the
    file's contents) so the source can always be traced later.
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
    """What the build produced, so other commands can report on it."""

    pack_path: Path
    manifest_path: Path
    records: list[SourceRecord] = field(default_factory=list)

    @property
    def converted_count(self) -> int:
        return sum(1 for r in self.records if r.converted)

    @property
    def skipped_count(self) -> int:
        return sum(1 for r in self.records if not r.converted)


def _checksum(data: bytes) -> str:
    """Return a short fingerprint of file contents (first 12 hex characters)."""
    return hashlib.sha256(data).hexdigest()[:12]


def _gather_files(source_dir: Path, work_dir: Path) -> list[Path]:
    """Find every usable file, unpacking any ZIP files we meet along the way.

    Nested ZIPs are handled: a ZIP inside a folder, and a ZIP inside a ZIP,
    are both expanded so their contents can be read.
    """
    found: list[Path] = []

    def walk(directory: Path) -> None:
        for item in sorted(directory.rglob("*")):
            if item.is_dir():
                continue
            if item.suffix.lower() == ".zip":
                extract_to = work_dir / (item.stem + "_unzipped")
                extract_to.mkdir(parents=True, exist_ok=True)
                try:
                    with zipfile.ZipFile(item) as zf:
                        zf.extractall(extract_to)
                except zipfile.BadZipFile:
                    continue
                walk(extract_to)
            else:
                found.append(item)

    walk(source_dir)
    return found


def build_pack(
    source_dir: str | Path,
    output_path: str | Path | None = None,
    goal: str = "",
) -> BuildResult:
    """Build a content pack from a folder of source files.

    Arguments:
        source_dir: the folder that holds your teaching files. It may contain
            sub-folders and ZIP files.
        output_path: where to write the content pack. Defaults to
            'content-pack.md' inside the source folder's parent.
        goal: an optional one-line teaching goal, recorded at the top of the
            pack so readers know what it is for.

    Returns a BuildResult describing what was written.
    """
    source_dir = Path(source_dir).expanduser().resolve()
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source folder not found: {source_dir}")

    md = _require_markitdown()

    if output_path is None:
        output_path = source_dir.parent / "content-pack.md"
    output_path = Path(output_path).expanduser().resolve()
    manifest_path = output_path.with_name(output_path.stem + "-manifest.md")

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        files = _gather_files(source_dir, work_dir)

        records: list[SourceRecord] = []
        sections: list[str] = []

        for path in files:
            try:
                rel = path.relative_to(source_dir)
            except ValueError:
                rel = Path(path.name)
            data = path.read_bytes()
            suffix = path.suffix.lower()
            record = SourceRecord(
                name=path.name,
                relative_path=str(rel),
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
            sections.append(_format_section(record, text))

        _write_pack(output_path, goal, source_dir, records, sections)
        _write_manifest(manifest_path, goal, source_dir, records)

    return BuildResult(
        pack_path=output_path,
        manifest_path=manifest_path,
        records=records,
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


def _write_pack(
    output_path: Path,
    goal: str,
    source_dir: Path,
    records: list[SourceRecord],
    sections: list[str],
) -> None:
    today = _dt.date.today().isoformat()
    converted = [r for r in records if r.converted]
    lines = [
        "# Educational Content Training Pack",
        "",
        "This file was built by Markdown Mentor from your source files.",
        "It is the content an AI chatbot will read. Each source below is "
        "wrapped in START and END markers so the AI can tell them apart.",
        "",
        f"- Built on: {today}",
        f"- Sources folder: {source_dir.name}",
        f"- Sources included: {len(converted)}",
        f"- Sources skipped: {len(records) - len(converted)}",
    ]
    if goal:
        lines += ["", f"**Teaching goal:** {goal}"]
    lines += ["", "---", ""]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n" + "\n".join(sections), encoding="utf-8")


def _write_manifest(
    manifest_path: Path,
    goal: str,
    source_dir: Path,
    records: list[SourceRecord],
) -> None:
    """Write a human-readable list of every file we looked at."""
    lines = [
        "# Source Manifest",
        "",
        "This is a plain list of every file Markdown Mentor found in your "
        "sources folder, and what happened to it.",
        "",
        f"- Sources folder: {source_dir}",
    ]
    if goal:
        lines += [f"- Teaching goal: {goal}"]
    lines += [
        "",
        "| File | Type | Size (bytes) | Fingerprint | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in records:
        status = "included" if r.converted else (r.note or "skipped")
        lines.append(
            f"| {r.relative_path} | {r.suffix or '(none)'} | {r.size_bytes} "
            f"| {r.checksum} | {status} |"
        )
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
