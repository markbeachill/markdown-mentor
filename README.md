# Markdown Mentor

Make Markdown library files, then use them to create teaching materials with the help of AI.

The project now has two public parts:

1. **Markdown Library Maker** makes one structured Markdown file from many source files. This is useful in teaching, research, project work, writing, policy work, and any other context where you want to give an AI a clean source library.
2. **Markdown Mentor** uses a Markdown library file to help teachers, tutors, lecturers, students, and self-directed learners plan, draft, and export teaching materials.

Markdown Mentor does not talk to an AI itself. It gives you structured source files and clear prompts. You use those prompts in your own AI chatbot.

## What each part does

### Markdown Library Maker

- **Makes a new Markdown library file.** It converts a folder, ZIP, or source file into one tidy Markdown file an AI can read.
- **Adds more sources.** It can add a file, folder, or ZIP to an existing Markdown library file.
- **Lists sources.** It shows which sources are inside a library file.
- **Checks the file structure.** It checks that the source markers are present and balanced.

### Markdown Mentor

- **Checks a library for teaching use.** It points out likely teaching risks, such as thin coverage, missing examples, missing practice, or private data.
- **Guides the teaching workflow.** It points you to the right prompts and library files for each step.
- **Exports finished materials.** It turns Markdown teaching materials into Word, PowerPoint, HTML, and PDF files. PDF export needs LibreOffice.

## Who does what

- **You** collect the sources, choose what to teach, and approve the plan.
- **Markdown Library Maker** makes and updates the source library file.
- **Markdown Mentor** checks, guides, and exports.
- **The AI** proposes, plans, and drafts when you paste a prompt into a chatbot.

## Quick command examples

Make a general Markdown library file:

```bash
markdown-library make ./my-sources -o my-library.md
```

Add more sources later:

```bash
markdown-library add my-library.md ./more-sources
```

Use the teaching workflow:

```bash
markdown-mentor start
```

Check a library/content pack for teaching use:

```bash
markdown-mentor check-pack my-library.md -g "teach thesis statements"
```

Export finished Markdown teaching materials:

```bash
markdown-mentor export ./materials -f docx
```

The older command still works as a teaching alias:

```bash
markdown-mentor build-pack ./my-sources
```

That command makes an **Educational Content Training Pack**. It uses the same underlying format as a Markdown library file.

## The teaching workflow

The quickest way to learn the workflow is the guided command. It runs the software steps for you and points you to the right prompt for each AI step:

```bash
markdown-mentor start
```

The full workflow is:

1. Collect your source files.
2. Make a Markdown library file.
3. Check whether the library is good enough for the teaching goal.
4. Decide what to teach.
5. Choose how to teach it.
6. Choose which materials to make.
7. Plan the materials.
8. Generate each material.
9. Export the finished Markdown files.

There is a full walkthrough in `docs/workflow.md` and the website in `site/`.

## Installing

Markdown Mentor is currently a small local prototype, not a normal app with a double-click installer. The command-line instructions are for testers and technical users.

For the clearest route, open `site/pages/install.html` in your browser or follow `docs/install-markitdown.md`. Those pages explain how to open a command window in the right folder.

The short technical version is:

```bash
python -m pip install "markitdown[all]"
python -m pip install -e .
markdown-library --version
markdown-mentor --version
```

Run the second command from the folder that contains this README and `pyproject.toml`.

## The website

The `site` folder is a small website you can open in a browser with no server. It explains both parts of the project:

- Markdown Library Maker
- Markdown Mentor

To open it on your own computer, open `site/index.html` in your web browser.

### Publishing the website with GitHub Pages

This repository includes a GitHub Actions workflow (`.github/workflows/publish-site.yml`) that publishes the `site` folder to GitHub Pages whenever the site changes on the `main` branch.

To switch it on, one time:

1. Push this repository to GitHub.
2. Go to the repository's **Settings**, then **Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.

After that, every change to the `site` folder on `main` publishes automatically. The published address will be `https://markbeachill.github.io/markdown-mentor/`.

The workflow uploads the `site` folder as-is. There is nothing to build: the site is plain HTML, CSS, and JavaScript. You can also run the workflow by hand from the repository's **Actions** tab.

## What is honest about this tool

- Ordinary users should not need to clone a repo or run commands forever. This is an early tester route, not the final product experience.
- The readiness check is a simple, rule-based helper, not an AI judgement. Treat it as a second pair of eyes.
- AI drafts may contain mistakes. Always read and edit what the AI produces.
- PDF export works if you have LibreOffice installed. If you do not, export to Word or HTML and use "Save as PDF" in your own software.

## Running the tests

The export step has a test suite, since export is where a hidden bug would cost the most rework. To run it:

```bash
python -m pip install -e ".[dev]"
pytest
```

## The library

The `library` folder holds ready-made files you can copy and adapt: a sample content pack, a sample Teaching Brief, five Pedagogy Specifications (school, ESL/EFL, undergraduate, primary, vocational), a Teaching Material Specifications catalogue, four Teaching Materials Lists (getting started, revision, tutor session, practical lesson), four prompts, two style profiles, and a source collection guide. You can build more style profiles on the website's Style page, with no need to edit JSON by hand.

## Licence

MIT. See `LICENSE`.
