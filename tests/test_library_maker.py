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

from markdown_mentor.build_pack import build_library


def _library_text(name: str, fingerprint: str, body: str) -> str:
    delim = "=" * 70
    return (
        "<!-- markdown-library-file: true -->\n"
        "# Markdown Library File\n\n"
        f"{delim}\nSOURCE START\nFile: {name}\nFingerprint: {fingerprint}\n{delim}\n\n"
        f"{body}\n"
        f"{delim}\nSOURCE END: {name}\n{delim}\n"
    )


def test_build_library_imports_existing_library_as_separate_sources(tmp_path: Path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "old-library.md").write_text(_library_text("one.md", "abc123", "One"), encoding="utf-8")

    result = build_library(sources, tmp_path / "new-library.md")

    text = result.pack_path.read_text(encoding="utf-8")
    assert "<!-- markdown-library-file: true -->" in text
    assert "SOURCE START" in text
    assert "File: one.md" in text
    assert "old-library.md" not in text.split("---", 1)[-1]
    assert result.converted_count == 1


def test_build_library_skips_duplicate_imported_sources_by_default(tmp_path: Path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "library-a.md").write_text(_library_text("one.md", "abc123", "One"), encoding="utf-8")
    (sources / "library-b.md").write_text(_library_text("copy-of-one.md", "abc123", "One again"), encoding="utf-8")

    result = build_library(sources, tmp_path / "new-library.md")

    text = result.pack_path.read_text(encoding="utf-8")
    assert text.count("SOURCE START") == 1
    assert any(r.note.startswith("not added:") for r in result.records)
    manifest = result.manifest_path.read_text(encoding="utf-8")
    assert "not added: duplicate source fingerprint" in manifest


def test_build_library_allows_duplicate_imported_sources_with_switch(tmp_path: Path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "library-a.md").write_text(_library_text("one.md", "abc123", "One"), encoding="utf-8")
    (sources / "library-b.md").write_text(_library_text("copy-of-one.md", "abc123", "One again"), encoding="utf-8")

    result = build_library(sources, tmp_path / "new-library.md", allow_duplicates=True)

    text = result.pack_path.read_text(encoding="utf-8")
    assert text.count("SOURCE START") == 2
    assert result.converted_count == 2
