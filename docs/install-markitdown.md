# Installing MarkItDown

Markdown Mentor needs MarkItDown to read your source files. MarkItDown is a
free tool from Microsoft that turns Word, PDF, PowerPoint, and other files into
Markdown. This page explains how to install it, step by step. You do not need
to be technical.

## What this page is about

How to put MarkItDown on your computer so Markdown Mentor can use it.

## Why it matters

Without MarkItDown, Markdown Mentor cannot read your source files, so it cannot
build a content pack. There is no fallback: this step is required.

## What you should do next

Follow the steps below in order. Each step says what to type and what you
should see.

---

## Step 1: Check you have Python

MarkItDown needs Python 3.10 or newer. Python is a free programming language
that the tool runs on.

Open a terminal:

- **Windows:** press the Start button, type `cmd`, and open "Command Prompt".
- **Mac:** open the "Terminal" app (in Applications, then Utilities).
- **Linux:** open your "Terminal" app.

In the terminal, type this and press Enter:

```bash
python --version
```

If you see a version number that is 3.10 or higher (for example `Python
3.12.1`), you are ready. Go to Step 2.

If you see an error, or a version lower than 3.10, install Python first from
the official site: https://www.python.org/downloads/ . On Windows, tick the box
that says "Add Python to PATH" during installation. Then close and reopen the
terminal and try `python --version` again.

> On some computers the command is `python3` instead of `python`. If `python`
> does not work, try `python3` everywhere on this page.

## Step 2: Install MarkItDown

In the same terminal, type this and press Enter:

```bash
pip install "markitdown[all]"
```

This downloads and installs MarkItDown and the extra parts that let it read
many file types. It may take a minute. You will see lines of text scroll past.
When it finishes, you are back at a normal prompt.

> If `pip` is not found, try `python -m pip install "markitdown[all]"` instead
> (or `python3 -m pip ...`).

## Step 3: Check it worked

Type this and press Enter:

```bash
python -c "import markitdown; print('MarkItDown is installed')"
```

If you see `MarkItDown is installed`, you are done. If you see an error, see
the help below.

## If something goes wrong

- **"pip is not recognised" or "command not found".** Python may not be
  installed, or not added to your PATH. Reinstall Python from
  https://www.python.org/downloads/ and tick "Add Python to PATH" on Windows.
- **A permissions error.** Try adding `--user` to the install command:
  `pip install --user "markitdown[all]"`.
- **It installed but Markdown Mentor still says MarkItDown is missing.** You may
  have more than one Python on your computer. Use the same Python command for
  both MarkItDown and Markdown Mentor.

## Official MarkItDown documentation

For more detail, see Microsoft's own pages:

- Source code and full guide: https://github.com/microsoft/markitdown
- The package on PyPI (where pip gets it): https://pypi.org/project/markitdown/

MarkItDown is made by Microsoft, not by Markdown Mentor. The links above are
the official place to check for updates and report problems with MarkItDown
itself.
