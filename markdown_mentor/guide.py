"""A guided walk through the Markdown Mentor teaching workflow.

The guide does not talk to an AI itself. It tells the user which folders, files,
and prompts to use. Python makes and exports files. AI and the user make
teaching judgements.
"""

from __future__ import annotations

from pathlib import Path


def _pause(message: str = "Press Enter to continue, or type 's' then Enter to skip: ") -> str:
    try:
        return input(message).strip().lower()
    except EOFError:
        return ""


def _say(text: str = "") -> None:
    print(text)


def _rule() -> None:
    print("-" * 64)


def _is_project_folder(path: Path) -> bool:
    return path.is_dir() and (path / "1-source-files").exists() and (path / "3-teaching-approach").exists()


def run_guide(project_or_library: str | None = None) -> int:
    """Walk the user through the canonical workflow. Returns an exit code."""
    project: Path | None = None
    library_path: Path | None = None

    if project_or_library:
        candidate = Path(project_or_library).expanduser().resolve()
        if _is_project_folder(candidate):
            project = candidate
        elif candidate.is_file():
            library_path = candidate
        elif candidate.exists():
            _say(f"Warning: {candidate} exists, but it does not look like a Markdown Mentor project folder.")

    _rule()
    _say("Markdown Mentor: guided teaching workflow")
    _say("The easiest route is to work inside one project folder.")
    _say("Make one with:  markdown-mentor new-project my-project")
    _say("The AI steps happen in your own chatbot. This tool never sends files to AI.")
    _rule()

    if not project and not library_path:
        try:
            answer = input("Path to your project folder, or leave blank to read the guide: ").strip()
        except EOFError:
            answer = ""
        if answer:
            candidate = Path(answer).expanduser().resolve()
            if _is_project_folder(candidate):
                project = candidate
            elif candidate.is_file():
                library_path = candidate
            else:
                _say(f"Warning: not found, or not a Markdown Mentor project folder: {candidate}")

    source_dir = project / "1-source-files" if project else Path("1-source-files")
    library_file = project / "2-markdown-library" / "markdown-library.md" if project else (library_path or Path("2-markdown-library/markdown-library.md"))
    teaching_approach = project / "3-teaching-approach" / "teaching-approach.md" if project else Path("3-teaching-approach/teaching-approach.md")
    materials_pack = project / "4-teaching-materials-pack" / "teaching-materials-pack.md" if project else Path("4-teaching-materials-pack/teaching-materials-pack.md")
    draft_dir = project / "5-draft-materials" if project else Path("5-draft-materials")
    export_dir = project / "6-final-exports" if project else Path("6-final-exports")
    style_file = project / "style" / "style.md" if project else Path("style/style.md")

    p_more_sources = project / "1-source-files" / "prompt-find-more-source-materials.md" if project else Path("1-source-files/prompt-find-more-source-materials.md")
    p_create_approach = project / "3-teaching-approach" / "prompt-create-teaching-approach.md" if project else Path("3-teaching-approach/prompt-create-teaching-approach.md")
    p_check_approach = project / "3-teaching-approach" / "prompt-check-teaching-approach.md" if project else Path("3-teaching-approach/prompt-check-teaching-approach.md")
    p_create_materials = project / "4-teaching-materials-pack" / "prompt-create-teaching-materials.md" if project else Path("4-teaching-materials-pack/prompt-create-teaching-materials.md")

    _say("\nA. Create and develop your source materials library")
    _say("\nStep 1 of 11  -  Create a project folder  [markdown-mentor]")
    if project:
        _say(f"Project folder: {project}")
    else:
        _say("Recommended command:  markdown-mentor new-project my-project")
    _pause()

    _say("\nStep 2 of 11  -  Collect source materials  [you]")
    _say(f"Put the source files in: {source_dir}")
    _say("Files can include Word, PDF, PowerPoint, Markdown, text, HTML, and ZIP files.")
    _pause()

    _say("\nStep 3 of 11  -  Ask AI what other source materials may help  [optional]")
    _say(f"Use this prompt if your source folder feels thin: {p_more_sources}")
    _pause()

    _say("\nStep 4 of 11  -  Make the Markdown library file  [make-markdown-library]")
    _say("Run this from inside the project folder:")
    _say("  make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md")
    _say(f"The library file will live at: {library_file}")
    _say("The tool processes folders, files, ZIPs, and nested ZIPs.")
    _say("This is a mechanical file-making step. It does not decide what the sources are good for.")
    _pause()

    _say("\nStep 5 of 11  -  List or remove files from the library  [optional]")
    _say("List sources:")
    _say("  make-markdown-library list 2-markdown-library/markdown-library.md")
    _say("Remove the third listed source:")
    _say("  make-markdown-library remove-file 2-markdown-library/markdown-library.md 3")
    _pause()

    _say("\nB. Plan your teaching approach")
    _say("\nStep 6 of 11  -  Create or customise the teaching approach file  [you + AI]")
    _say(f"Teaching approach file: {teaching_approach}")
    _say("It has four sections: What to teach, Aims of teaching, Who is being taught, How to teach.")
    _say(f"If using AI, upload {library_file} and use: {p_create_approach}")
    _pause()

    _say("\nStep 7 of 11  -  Check the teaching approach against the library  [AI, checked by you]")
    _say(f"Use: {p_check_approach}")
    _say("This is a teaching judgement. Python cannot do it honestly.")
    _say("Edit and save the final approach file afterwards.")
    _pause()

    _say("\nStep 8 of 11  -  Choose and customise a teaching materials pack  [you]")
    _say(f"Materials pack file: {materials_pack}")
    _say("This file says what outputs to make, such as a handout, slides, or a worksheet with answer guidance.")
    _pause()

    _say("\nC. Create your teaching materials")
    _say("\nStep 9 of 11  -  Ask AI to create separate Markdown teaching files  [AI, checked by you]")
    _say("Give the AI the library file, teaching approach file, and teaching materials pack.")
    _say(f"Use: {p_create_materials}")
    _say(f"Save each Markdown material in: {draft_dir}")
    _pause()

    _say("\nStep 10 of 11  -  Choose or customise your Markdown style file  [you]")
    _say(f"Style file: {style_file}")
    _say("This is a Markdown file. The export tool applies the settings it understands.")
    _pause()

    _say("\nStep 11 of 11  -  Process the materials into styled output  [markdown-mentor]")
    _say("Recommended command from inside the project folder:")
    _say("  markdown-mentor export 5-draft-materials -f docx -o 6-final-exports -s style/style.md")
    try:
        do_export = input("Export now? Type y then Enter, or press Enter to skip: ").strip().lower()
    except EOFError:
        do_export = ""
    if do_export == "y":
        if draft_dir.exists():
            try:
                fmt = input("Format (docx, pptx, html, pdf) [docx]: ").strip().lower() or "docx"
                from .export import export_path
                res = export_path(draft_dir, fmt, export_dir, style_file if style_file.exists() else None)
                _say(f"Converted {len(res.outputs)} file(s) to {fmt.upper()} in {export_dir}.")
                for src, dst in zip(res.inputs, res.outputs):
                    _say(f"  {src.name}  ->  {dst}")
            except (FileNotFoundError, ValueError) as exc:
                _say(f"Problem: {exc}")
        else:
            _say(f"That folder was not found: {draft_dir}")
    else:
        _say("Skipped. Run the export command when your draft materials are ready.")

    _rule()
    _say("Done. Read and edit everything the AI produced before teaching from it.")
    _rule()
    return 0
