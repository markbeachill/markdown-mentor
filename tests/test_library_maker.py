from pathlib import Path

from markdown_mentor.build_pack import check_library_format, list_library_sources


def test_list_library_sources_reads_source_markers(tmp_path: Path):
    library = tmp_path / "library.md"
    library.write_text(
        "# Markdown Library File\n\n"
        "======================================================================\n"
        "SOURCE START\n"
        "File: one.md\n"
        "Fingerprint: abc123\n"
        "======================================================================\n"
        "\nSource text\n"
        "======================================================================\n"
        "SOURCE END: one.md\n"
        "======================================================================\n",
        encoding="utf-8",
    )

    assert list_library_sources(library) == ["one.md"]


def test_check_library_format_spots_unbalanced_markers(tmp_path: Path):
    library = tmp_path / "broken.md"
    library.write_text(
        "# Markdown Library File\n\n"
        "SOURCE START\n"
        "File: one.md\n"
        "Fingerprint: abc123\n",
        encoding="utf-8",
    )

    report = check_library_format(library)

    assert report.source_count == 1
    assert not report.looks_valid
    assert any("do not match" in issue for issue in report.issues)
