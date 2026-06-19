#!/usr/bin/env python3
"""Download the Markdown Mentor user scripts and set up this folder.

Put this file in a new folder for your project, then run:

    python setup-markdown-mentor.py

The script downloads:
- make-markdown-library.py
- make-teaching-materials.py

Then it runs:

    python make-markdown-library.py setup

It only changes the folder where you run it. It does not upload your files.
"""

from __future__ import annotations

import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://markbeachill.github.io/markdown-mentor/downloads/"
FILES = [
    "make-markdown-library.py",
    "make-teaching-materials.py",
]


def download_file(name: str, target: Path) -> bool:
    url = BASE_URL + name
    print(f"Downloading {name}...")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"Problem: could not download {url}")
        print(f"Reason: {exc}")
        return False
    target.write_bytes(data)
    print(f"  saved {target.name}")
    return True


def main() -> int:
    here = Path.cwd()
    print("Markdown Mentor setup")
    print("This will work in this folder only:")
    print(f"  {here}")
    print()
    print("It will download the two user scripts and create the project folders.")
    print("It will not upload your files.")
    print()

    ok = True
    for name in FILES:
        ok = download_file(name, here / name) and ok

    if not ok:
        print()
        print("Setup could not finish because one or more files could not be downloaded.")
        print("You can download the files manually from:")
        print(f"  {BASE_URL}")
        return 1

    print()
    print("Creating the project folders and starter files...")
    result = subprocess.run([sys.executable, "make-markdown-library.py", "setup"], check=False)
    if result.returncode != 0:
        print("Problem: the project folders could not be created.")
        return result.returncode

    print()
    print("Setup complete.")
    print("Next step:")
    print("  1. Put your source files in 1-source-files/")
    print("  2. Run: python make-markdown-library.py make")
    print("     or: python make-markdown-library.py make 1-source-files 2-markdown-library")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
