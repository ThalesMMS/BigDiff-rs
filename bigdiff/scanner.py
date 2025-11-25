#
# scanner.py
# BigDiff
#
# Walks directory trees, applying ignore patterns to collect file and directory listings for comparison.
#
# Thales Matheus Mendonça Santos - November 2025
from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Sequence, Set

DEFAULT_IGNORES = {".git", "__pycache__", ".DS_Store", "Thumbs.db"}


@dataclass
class ScanResult:
    files: Dict[Path, Path]       # relpath -> abspath
    dirs: Set[Path]               # set of relative directories
    roots: Path


def scan_dir(root: Path, ignore_patterns: Sequence[str]) -> ScanResult:
    files: Dict[Path, Path] = {}
    dirs: Set[Path] = set()
    patterns = [p.strip() for p in ignore_patterns if p.strip()]
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # Filter ignored folders in-place so os.walk does not descend into them.
        dirnames[:] = [d for d in dirnames if not is_ignored(Path(d), patterns)]
        for d in dirnames:
            rel = Path(os.path.relpath(os.path.join(dirpath, d), root))
            if not is_ignored(rel, patterns):
                dirs.add(rel)
        for fn in filenames:
            rel = Path(os.path.relpath(os.path.join(dirpath, fn), root))
            if is_ignored(rel, patterns):
                continue
            files[rel] = root / rel
    return ScanResult(files=files, dirs=dirs, roots=root)


def is_ignored(rel: Path, patterns: Sequence[str]) -> bool:
    # Ignore well-known noise directories/files first.
    if rel.name in DEFAULT_IGNORES:
        return True
    # Apply glob patterns against both the relative path and the basename.
    s_rel = str(rel).replace("\\", "/")
    for pat in patterns:
        pat = pat.strip()
        if not pat:
            continue
        # Allow comma-separated patterns in a single CLI argument.
        for subpat in pat.split(","):
            sp = subpat.strip()
            if not sp:
                continue
            if fnmatch.fnmatch(s_rel, sp) or fnmatch.fnmatch(rel.name, sp):
                return True
    return False
