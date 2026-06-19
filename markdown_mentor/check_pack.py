"""Check whether a Markdown library/content pack is ready to teach from.

Plain English: this looks at a Markdown library file and points out likely
teaching problems before you ask an AI to build teaching materials from it. A
thin or messy source library usually leads to thin or messy materials.

Who does what:
- Markdown Mentor (this code) runs the check and writes a readiness note.
- The user reads the note and decides whether to add more sources first.

This check never stops you from continuing. It only makes the risks visible.
It is a simple, rule-based check, not an AI judgement. Treat it as a helpful
second pair of eyes, not the final word.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .build_pack import DELIMITER


@dataclass
class Finding:
    """One thing worth knowing about the pack."""

    level: str  # "ok", "watch", or "risk"
    message: str


@dataclass
class ReadinessReport:
    source_count: int = 0
    word_count: int = 0
    findings: list[Finding] = field(default_factory=list)
    note_path: Path | None = None

    @property
    def risk_count(self) -> int:
        return sum(1 for f in self.findings if f.level == "risk")

    @property
    def watch_count(self) -> int:
        return sum(1 for f in self.findings if f.level == "watch")


# Words that hint a kind of content is present. Lower case, matched loosely.
_EXAMPLE_HINTS = ("example", "worked example", "for instance", "e.g.", "sample")
_QUESTION_HINTS = ("?", "question", "quiz", "exercise", "practice", "task")
_ASSESSMENT_HINTS = (
    "mark scheme", "marking", "assessment criteria", "rubric",
    "grade", "success criteria", "learning objective",
)
# Patterns that may mean private personal data is present.
_PRIVACY_PATTERNS = (
    r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",            # email address
    r"\b\d{3}[\s.]\d{3,4}[\s.]\d{3,4}\b",        # phone-like number
    r"\bstudent (?:id|number)\b",
    r"\bdate of birth\b",
)


def _split_sources(text: str) -> list[str]:
    """Split the pack back into its source sections using the markers."""
    chunks = []
    current: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.strip() == "SOURCE START":
            inside = True
            current = []
            continue
        if line.startswith("SOURCE END"):
            if current:
                chunks.append("\n".join(current))
            inside = False
            current = []
            continue
        if inside and line.strip() != DELIMITER and not line.startswith("File:") \
                and not line.startswith("Fingerprint:"):
            current.append(line)
    return chunks


def check_pack(pack_path: str | Path, goal: str = "") -> ReadinessReport:
    """Run the readiness check on a content pack file.

    Arguments:
        pack_path: the Markdown library/content pack file to check.
        goal: an optional teaching goal, used to tailor the wording.

    Returns a ReadinessReport. A readiness note is also written next to the
    pack as '<pack-name>-readiness.md'.
    """
    pack_path = Path(pack_path).expanduser().resolve()
    if not pack_path.is_file():
        raise FileNotFoundError(f"Markdown library/content pack not found: {pack_path}")

    full_text = pack_path.read_text(encoding="utf-8")
    sources = _split_sources(full_text)
    # Only judge the source content itself, never the pack's own header/markers.
    text = "\n".join(sources)
    lower = text.lower()
    words = re.findall(r"\b\w+\b", text)

    report = ReadinessReport(source_count=len(sources), word_count=len(words))

    # 1. How much content is there?
    if len(sources) == 0:
        report.findings.append(Finding(
            "risk",
            "The pack has no readable sources. Build it again from a folder "
            "that contains supported files.",
        ))
    elif len(sources) == 1:
        report.findings.append(Finding(
            "watch",
            "The pack has only one source. One source can support a short "
            "overview, but rarely a full set of materials.",
        ))
    else:
        report.findings.append(Finding(
            "ok", f"The pack has {len(sources)} sources."
        ))

    if report.word_count < 400 and sources:
        report.findings.append(Finding(
            "risk",
            "There is very little text in the pack (under 400 words). The AI "
            "will have little to work from. Add fuller sources.",
        ))
    elif report.word_count < 1500 and sources:
        report.findings.append(Finding(
            "watch",
            "The pack is fairly short (under 1500 words). It may only support "
            "a narrow teaching brief.",
        ))

    # 2. Are the building blocks of good teaching present?
    if not any(h in lower for h in _EXAMPLE_HINTS):
        report.findings.append(Finding(
            "watch",
            "No clear examples found. Worked examples help the AI produce "
            "concrete materials. Consider adding some.",
        ))
    if not any(h in lower for h in _QUESTION_HINTS):
        report.findings.append(Finding(
            "watch",
            "No questions or practice tasks found. Without these, generated "
            "quizzes and worksheets may be weak.",
        ))
    if not any(h in lower for h in _ASSESSMENT_HINTS):
        report.findings.append(Finding(
            "watch",
            "No assessment or marking information found. Add success criteria "
            "or a mark scheme if you want materials that match how work is judged.",
        ))

    # 3. Duplicates (same source appearing more than once).
    fingerprints = re.findall(r"Fingerprint: (\w+)", full_text)
    seen: set[str] = set()
    dupes: set[str] = set()
    for fp in fingerprints:
        if fp in seen:
            dupes.add(fp)
        seen.add(fp)
    if dupes:
        report.findings.append(Finding(
            "watch",
            f"{len(dupes)} source(s) appear to be duplicates (same content "
            "included more than once). Remove repeats to avoid skewing the AI.",
        ))

    # 4. Possible private personal data.
    privacy_hits = 0
    for pattern in _PRIVACY_PATTERNS:
        privacy_hits += len(re.findall(pattern, text, flags=re.IGNORECASE))
    if privacy_hits:
        report.findings.append(Finding(
            "risk",
            f"The pack may contain private personal data ({privacy_hits} "
            "possible match(es), such as emails, phone numbers, or student IDs). "
            "Check and remove anything that should not be shared with an AI.",
        ))

    if not any(f.level == "risk" for f in report.findings):
        report.findings.append(Finding(
            "ok",
            "No blocking problems found. Read the watch items below before you "
            "continue.",
        ))

    report.note_path = _write_note(pack_path, goal, report)
    return report


def _write_note(pack_path: Path, goal: str, report: ReadinessReport) -> Path:
    note_path = pack_path.with_name(pack_path.stem + "-readiness.md")
    order = {"risk": 0, "watch": 1, "ok": 2}
    label = {"risk": "Risk", "watch": "Worth checking", "ok": "Looks fine"}
    findings = sorted(report.findings, key=lambda f: order[f.level])

    lines = [
        "# Content Pack Readiness Note",
        "",
        "This note lists possible teaching problems with your Markdown library/content pack. It does not "
        "stop you from continuing. Use it to decide whether to add or fix "
        "sources before you build teaching materials.",
        "",
        f"- Sources in pack: {report.source_count}",
        f"- Approximate words: {report.word_count}",
        f"- Risks: {report.risk_count}",
        f"- Things worth checking: {report.watch_count}",
    ]
    if goal:
        lines += [f"- Teaching goal: {goal}"]
    lines += ["", "## Findings", ""]
    for f in findings:
        lines.append(f"- **{label[f.level]}:** {f.message}")
    lines += [
        "",
        "## What to do next",
        "",
        "1. If there are risks, fix those first. Privacy risks matter most: "
        "never share private student data with an AI.",
        "2. Look at the watch items. Add examples, questions, or assessment "
        "material if they are missing and you need them.",
        "3. When you are happy, move on to writing your Teaching Brief.",
    ]
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return note_path
