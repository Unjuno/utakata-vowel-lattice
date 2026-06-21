#!/usr/bin/env python
"""Local environment and repository health check."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

REQUIRED_DIRS = [
    "data/raw",
    "data/interim",
    "data/processed",
    "outputs",
    "outputs/analysis",
    "outputs/audio",
    "assets/carriers",
]

REQUIRED_MODULES = [
    "utakata_vowel_lattice",
    "utakata_vowel_lattice.phonology",
    "utakata_vowel_lattice.entropy",
    "utakata_vowel_lattice.overlap_markov",
]


def check_python() -> bool:
    ok = sys.version_info >= (3, 11)
    status = "ok" if ok else "fail"
    print(f"[{status}] python >= 3.11: {sys.version.split()[0]}")
    return ok


def ensure_dirs() -> bool:
    for name in REQUIRED_DIRS:
        Path(name).mkdir(parents=True, exist_ok=True)
        print(f"[ok] directory: {name}")
    return True


def check_imports() -> bool:
    ok = True
    for name in REQUIRED_MODULES:
        try:
            importlib.import_module(name)
            print(f"[ok] import: {name}")
        except Exception as exc:  # pragma: no cover - diagnostic path
            ok = False
            print(f"[fail] import: {name}: {exc}")
    return ok


def check_gitignored_paths() -> bool:
    # This is a lightweight reminder, not a full gitignore parser.
    ignored_like = ["outputs", "data/raw", "data/interim", "data/processed"]
    for name in ignored_like:
        print(f"[info] expected git-ignored path: {name}")
    return True


def main() -> int:
    checks = [check_python(), ensure_dirs(), check_imports(), check_gitignored_paths()]
    if all(checks):
        print("doctor: ok")
        return 0
    print("doctor: failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
