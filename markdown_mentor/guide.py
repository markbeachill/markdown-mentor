"""A guided walk through the whole workflow, in the terminal.

Plain English: this command holds your hand through the nine steps. It runs the
teaching workflow steps for you (make the source library, check it, export) and, for the thinking
steps, it tells you exactly which prompt to open and what to paste. It never
talks to an AI itself. You stay in control: at each step you press Enter to go
on, or type 's' to skip.

Who does what:
- This command runs the source-library, teaching check, and export steps.
- It points you to the right prompt for each AI step.
- You do the AI steps in your own chatbot and save the results.
"""

from __future__ import annotations

from pathlib import Path

from .build_pack import build_pack, MarkItDownMissing
from .check_pack import check_pack


# Where the library lives, relative to the installed package. When run from a
# clone of the repository, the library sits next to the package folder.
def _library_root() -> Path:
    here = Path(__file__).resolve().parent
    candidate = here.parent / "library"
    return candidate


def _pause(message: str = "Press Enter to continue, or type 's' then Enter to skip: ") -> str:
    try:
        return input(message).strip().lower()
    except EOFError:
        return ""


def _say(text: str = "") -> None:
    print(text)


def _rule() -> None:
    print("-" * 64)


def run_guide(source_dir: str | None = None) -> int:
    """Walk the user through the workflow. Returns an exit code."""
    lib = _library_root()
    prompts = lib / "prompts"

    _rule()
    _say("Markdown Mentor: a guided run through the workflow.")
    _say("This walks you through all nine steps. The software steps run here.")
    _say("The thinking steps happen in your own AI chatbot; this points you to")
    _say("the right prompt each time. Nothing here talks to an AI for you.")
    _rule()

    # Step 1: sources
    _say("\nStep 1 of 9  -  Collect your sources  [you]")
    _say("Put the files you want to teach from into one folder.")
    if not source_dir:
        try:
            source_dir = input("Folder with your source files: ").strip()
        except EOFError:
            _say("No folder given. Stopping.")
            return 1
    source_path = Path(source_dir).expanduser()
    if not source_path.is_dir():
        _say(f"That folder was not found: {source_path}")
        return 1

    goal = ""
    try:
        goal = input("One-line teaching goal (optional): ").strip()
    except EOFError:
        goal = ""

    # Step 2: build
    _say("\nStep 2 of 9  -  Make the Markdown library file  [software]")
    if _pause() != "s":
        try:
            result = build_pack(source_path, None, goal)
        except MarkItDownMissing as exc:
            _say("\n" + str(exc))
            return 2
        _say(f"Made library/content pack: {result.pack_path}")
        _say(f"Manifest: {result.manifest_path}")
        _say(f"Sources included: {result.converted_count}, skipped: {result.skipped_count}")
        pack_path = result.pack_path
    else:
        pack_path = source_path.parent / "content-pack.md"
        _say("Skipped. Assuming the library/content pack is at: " + str(pack_path))

    # Step 3: check
    _say("\nStep 3 of 9  -  Check the library for teaching use  [software]")
    if _pause() != "s" and pack_path.is_file():
        report = check_pack(pack_path, goal)
        _say(f"Readiness note: {report.note_path}")
        _say(f"Risks: {report.risk_count}, worth checking: {report.watch_count}")
        if report.risk_count:
            _say("There are risks. Read the note before going on.")
            _say(f"If you want help improving the source library, use the prompt:")
            _say(f"  {prompts / 'improve-content-pack.md'}")
    else:
        _say("Skipped.")

    # Step 4: brief (AI)
    _say("\nStep 4 of 9  -  Decide what to teach  [you + AI]")
    _say("Write a Teaching Brief, or let the AI suggest some.")
    _say("To get suggestions, open this prompt, paste it into your chatbot,")
    _say("then paste your Markdown library/content pack:")
    _say(f"  {prompts / 'suggest-teaching-briefs.md'}")
    _say("Save your chosen brief as a Markdown file, for example brief.md.")
    _pause()

    # Step 5: pedagogy
    _say("\nStep 5 of 9  -  Choose how to teach it  [you]")
    _say("Pick a Pedagogy Specification from:")
    _say(f"  {lib / 'pedagogy-specs'}")
    _say("Copy one and edit it to match your learners.")
    _pause()

    # Step 6: materials list
    _say("\nStep 6 of 9  -  Choose which materials to make  [you]")
    _say("Pick a Teaching Materials List from:")
    _say(f"  {lib / 'materials-lists'}")
    _pause()

    # Step 7: inventory (AI)
    _say("\nStep 7 of 9  -  Plan the materials  [AI, checked by you]")
    _say("Open this prompt and paste it into your chatbot, then paste your")
    _say("Markdown library/content pack, brief, pedagogy, material specifications, and list:")
    _say(f"  {prompts / 'generate-inventory.md'}")
    _say("The AI returns a plan. Read it carefully. This is the main checkpoint.")
    _pause()

    # Step 8: generate (AI)
    _say("\nStep 8 of 9  -  Generate each material  [AI, checked by you]")
    _say("For each item in the plan, open this prompt and paste it into your")
    _say("chatbot with the pieces it asks for:")
    _say(f"  {prompts / 'generate-material.md'}")
    _say("Save each result as a Markdown file in one folder, for example")
    _say("'materials'. Make one file per material.")
    _pause()

    # Step 9: export
    _say("\nStep 9 of 9  -  Export  [software]")
    _say("Turn your finished Markdown into Word, slides, web, or PDF files.")
    try:
        materials_dir = input("Folder with your finished Markdown materials (or skip): ").strip()
    except EOFError:
        materials_dir = ""
    if materials_dir:
        m_path = Path(materials_dir).expanduser()
        if m_path.exists():
            try:
                fmt = input("Format (docx, pptx, html) [docx]: ").strip().lower() or "docx"
                out = input("Where to save them [exports]: ").strip() or "exports"
                from .export import export_path
                res = export_path(m_path, fmt, out, None)
                _say(f"Converted {len(res.outputs)} file(s) to {fmt.upper()} in {out}.")
                for src, dst in zip(res.inputs, res.outputs):
                    _say(f"  {src.name}  ->  {dst}")
            except (FileNotFoundError, ValueError) as exc:
                _say(f"Problem: {exc}")
        else:
            _say(f"That folder was not found: {m_path}")
    else:
        _say("Skipped. When ready, run:  markdown-mentor export <folder> -f docx")

    _rule()
    _say("That is the whole workflow. For PDF, install LibreOffice or open a Word")
    _say("or web file and use 'Save as PDF'. Read everything the AI produced.")
    _rule()
    return 0
