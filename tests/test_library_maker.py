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

from markdown_mentor.build_pack import remove_file_from_library


def test_remove_file_from_library_removes_by_number_and_makes_backup(tmp_path: Path):
    library = tmp_path / "library.md"
    delim = "=" * 70
    library.write_text(
        f"# Markdown Library File\n\n{delim}\nSOURCE START\nFile: one.md\nFingerprint: abc123\n{delim}\n\nOne\n{delim}\nSOURCE END: one.md\n{delim}\n\n"
        f"{delim}\nSOURCE START\nFile: two.md\nFingerprint: def456\n{delim}\n\nTwo\n{delim}\nSOURCE END: two.md\n{delim}\n",
        encoding="utf-8",
    )

    remove_file_from_library(library, 2)

    text = library.read_text(encoding="utf-8")
    assert "File: one.md" in text
    assert "File: two.md" not in text
    assert (tmp_path / "library.backup.md").is_file()
    assert (tmp_path / "library-manifest.md").is_file()
