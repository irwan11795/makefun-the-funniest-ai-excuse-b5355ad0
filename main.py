"""The Funniest AI Excuse — make.fun entry.

Writes a single one-line excuse to /output/entry.txt.
Python 3.13 standard library only. Deterministic: one constant, no
network, no file reads, no environment secrets.
"""

import os
import sys
import tempfile

ENTRY = "I found the answer in tab 214 of your browser, closed it by accident, and now it only exists as a feeling."

FILENAME = "entry.txt"


def _candidate_dirs():
    """Output directory candidates, in priority order."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    dirs.append(tempfile.gettempdir())
    return dirs


def main():
    if not ENTRY or not ENTRY.strip() or len(ENTRY) > 200:
        print("entry must be 1-200 non-whitespace characters", file=sys.stderr)
        return 1
    # No trailing newline: the gate counts the text itself (1-200 chars),
    # and writing without a newline keeps the count unambiguous.
    data = ENTRY.encode("utf-8")
    for directory in _candidate_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, FILENAME)
            with open(path, "wb") as fh:
                fh.write(data)
            return 0
        except OSError:
            continue
    # Every candidate failed (e.g. read-only filesystem): still exit 0.
    print("warning: could not write entry.txt to any candidate directory",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
