# Markdown Mentor

Turn teaching files into teaching materials, with the help of AI.

Markdown Mentor helps teachers, tutors, lecturers, students, and self-directed
learners turn a folder of source documents into useful teaching materials. It
does the parts a computer is good at. You and an AI chatbot do the thinking.

## What it does

- **Builds a content pack.** It converts your folder of files (Word, PDF,
  PowerPoint, and more) into one tidy Markdown file an AI can read. Markdown is
  a simple text format used for headings, lists, and links.
- **Checks the pack.** It points out likely problems, such as thin coverage or
  private data, before you build materials.
- **Exports finished materials.** It turns Markdown teaching materials into
  Word, PowerPoint, and web files.

The AI steps in between (suggesting what to teach, planning the materials, and
drafting them) are done by you, using any AI chatbot and the ready-made prompts
in the `library/prompts` folder. Markdown Mentor does not talk to any AI itself.

## Who does what

- **You** collect the sources, choose what to teach, and approve the plan.
- **Markdown Mentor** converts, checks, and exports.
- **The AI** proposes, plans, and drafts, when you paste a prompt into a chatbot.

## The workflow

The quickest way to learn the workflow is the guided command. It runs the
software steps for you and points you to the right prompt for each AI step:

```bash
markdown-mentor start
```

You can also run the steps yourself:

1. Collect your source files into one folder.
2. Build a content pack: `markdown-mentor build-pack ./my-sources`
3. Check the pack: `markdown-mentor check-pack ./content-pack.md`
4. Decide what to teach (write a Teaching Brief, or use the "suggest briefs" prompt).
5. Choose how to teach it (pick a Pedagogy Specification).
6. Choose which materials to make (pick a Teaching Materials List).
7. Plan the materials (use the "generate inventory" prompt, then check the plan).
8. Generate each material (use the "generate material" prompt, one at a time).
9. Save each material as a Markdown file.
10. Export: `markdown-mentor export ./materials -f docx`

There is a full walkthrough in `docs/workflow.md`.

## Installing

Markdown Mentor needs Python 3.10 or newer, and a free tool from Microsoft
called MarkItDown.

1. Install MarkItDown by following `docs/install-markitdown.md`.
2. Install Markdown Mentor:

   ```bash
   pip install -e .
   ```

   Run this from inside the `markdown-mentor` folder (the one with this README
   in it).

3. Check it worked:

   ```bash
   markdown-mentor --version
   ```

## The website

The `site` folder is a small website you can open in a browser with no server.
It explains the workflow and gives you the prompts in copy-ready blocks, with a
"Copy" button. To open it on your own computer, open `site/index.html` in your
web browser.

### Publishing the website with GitHub Pages

This repository includes a GitHub Actions workflow
(`.github/workflows/publish-site.yml`) that publishes the `site` folder to
GitHub Pages whenever the site changes on the `main` branch.

To switch it on, one time:

1. Push this repository to GitHub.
2. Go to the repository's **Settings**, then **Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.

After that, every change to the `site` folder on `main` publishes
automatically. The published address will be
`https://markbeachill.github.io/markdown-mentor/`.

The workflow uploads the `site` folder as-is. There is nothing to build: the
site is plain HTML, CSS, and JavaScript. You can also run the workflow by hand
from the repository's **Actions** tab.

## What is honest about this tool

- The readiness check is a simple, rule-based helper, not an AI judgement. Treat
  it as a second pair of eyes.
- AI drafts may contain mistakes. Always read and edit what the AI produces.
- PDF export works if you have LibreOffice installed (a free office suite). If
  you do not, export to Word or web and use "Save as PDF" in your own software.
  The tool tells you which applies.

## Running the tests

The export step has a test suite, since export is where a hidden bug would cost
the most rework. To run it:

```bash
pip install pytest
pytest
```

## The library

The `library` folder holds ready-made files you can copy and adapt: a sample
content pack, a sample Teaching Brief, five Pedagogy Specifications (school,
ESL/EFL, undergraduate, primary, vocational), a Teaching Material Specifications
catalogue, four Teaching Materials Lists (getting started, revision, tutor
session, practical lesson), four prompts, two style profiles, and a source
collection guide. You can build more style profiles on the website's Style
page, with no need to edit JSON by hand.

## Licence

MIT. See `LICENSE`.
