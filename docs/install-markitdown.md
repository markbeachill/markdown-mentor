# Installing the prototype

Markdown Library Maker and Markdown Mentor currently run as command-line tools. This is an early tester route, not the final ordinary-user experience.

The final product should not ask most teachers or learners to clone a repo or run commands. For now, testers need Python, MarkItDown, and this project folder.

## What this page is about

How to install Python, MarkItDown, Markdown Library Maker, and Markdown Mentor on your computer.

## Why it matters

Without MarkItDown, the tool cannot read Word, PDF, PowerPoint, HTML, and other source files.

## What you should do next

Follow the beginner tester route below. Use the technical notes only if you already know the command line.

---

## Step 1: Install Python

Python is the free program that runs the prototype.

1. Go to https://www.python.org/downloads/ .
2. Download the current Python 3 version.
3. Install it.
4. On Windows, tick **Add Python to PATH** before you click Install.

## Step 2: Get the project folder

For testers, the simplest route is to download the project as a ZIP file from GitHub.

1. Open the Markdown Mentor GitHub page.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Open your Downloads folder.
5. Extract the ZIP file.
6. Open the extracted folder until you can see `README.md` and `pyproject.toml`.

That folder is the project folder. Some commands must be run from that folder because Python needs to see `pyproject.toml`.

## Step 3: Open a command window in the project folder

On Windows:

1. Open the project folder in File Explorer.
2. Click the address bar at the top of the window.
3. Type `cmd`.
4. Press Enter.

This opens Command Prompt in the current folder.

On Mac:

1. Open Terminal.
2. Type `cd ` with a space after it.
3. Drag the project folder into the Terminal window.
4. Press Enter.

On Linux:

1. Open the project folder in your file manager.
2. Right-click inside the folder.
3. Choose **Open in Terminal**, if your desktop offers that option.

## Step 4: Check Python

Command to copy:

```bash
python --version
```

If you see something like `Python 3.12.1`, Python is ready. If the command is not found, try:

```bash
python3 --version
```

## Step 5: Install MarkItDown

Command to copy:

```bash
python -m pip install "markitdown[all]"
```

If you used `python3` earlier, use this instead:

```bash
python3 -m pip install "markitdown[all]"
```

## Step 6: Install the local prototype

Run this from the project folder, the folder that contains `README.md` and `pyproject.toml`.

Command to copy:

```bash
python -m pip install -e .
```

If you used `python3` earlier, use this instead:

```bash
python3 -m pip install -e .
```

## Step 7: Check it worked

Check Markdown Library Maker:

```bash
markdown-library --version
```

Check Markdown Mentor:

```bash
markdown-mentor --version
```

If both commands show a version number, the prototype is installed.

## Try the two tools

Make a source library:

```bash
markdown-library make examples/sample-sources -o content-pack.md
```

Start the teaching workflow:

```bash
markdown-mentor start
```

## If something goes wrong

- **The command is not recognised.** Python may not be installed correctly. On Windows, reinstall Python and tick **Add Python to PATH**.
- **`python` does not work.** Try `python3` instead.
- **`python -m pip` does not work.** Python may not have installed pip. Try reinstalling Python from python.org.
- **`python -m pip install -e .` fails.** Check that you are in the project folder. You should be able to see `README.md` and `pyproject.toml` in that folder.
- **A permissions error appears.** Try adding `--user` to the install command, for example `python -m pip install --user "markitdown[all]"`.

## Technical notes

The prototype currently requires Python 3.10 or newer. It installs as an editable local package with `python -m pip install -e .`. MarkItDown is installed from PyPI with the optional `[all]` extras so it can read more file types.

Useful commands:

```bash
python --version
python -m pip install "markitdown[all]"
python -m pip install -e .
markdown-library --version
markdown-mentor --version
```

## Official MarkItDown documentation

MarkItDown is made by Microsoft, not by Markdown Mentor. For more detail, see:

- Source code and full guide: https://github.com/microsoft/markitdown
- The package on PyPI: https://pypi.org/project/markitdown/
