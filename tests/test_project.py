from pathlib import Path

from markdown_mentor.project import new_project


def test_new_project_creates_standard_folders(tmp_path: Path):
    result = new_project(tmp_path / "demo")
    project = result.path

    assert (project / "README-FIRST.md").is_file()
    assert (project / "1-source-files" / "prompt-find-more-source-materials.md").is_file()
    assert (project / "2-markdown-library").is_dir()
    assert (project / "3-teaching-approach" / "teaching-approach.md").is_file()
    assert (project / "3-teaching-approach" / "prompt-create-teaching-approach.md").is_file()
    assert (project / "3-teaching-approach" / "prompt-check-teaching-approach.md").is_file()
    assert (project / "4-teaching-materials-pack" / "teaching-materials-pack.md").is_file()
    assert (project / "4-teaching-materials-pack" / "prompt-create-teaching-materials.md").is_file()
    assert (project / "5-draft-materials").is_dir()
    assert (project / "6-final-exports").is_dir()
    assert (project / "style" / "style.md").is_file()
    assert not (project / "prompts").exists()
    assert not (project / "examples").exists()


def test_new_project_does_not_overwrite_existing_readme(tmp_path: Path):
    project = tmp_path / "demo"
    project.mkdir()
    readme = project / "README-FIRST.md"
    readme.write_text("keep me", encoding="utf-8")

    new_project(project)

    assert readme.read_text(encoding="utf-8") == "keep me"
