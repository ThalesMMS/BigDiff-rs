#
# io_utils.py
# BigDiff
#
# Provides file utilities for size parsing, binary detection, resilient text reading, hashing, and name collision avoidance.
#
# Thales Matheus Mendonça Santos - November 2025
from __future__ import annotations

import hashlib
from pathlib import Path


def parse_size(s: str) -> int:
    """
    Convert strings like "5MB", "200k", or "10MiB" into byte counts.
    """
    s = s.strip().lower()
    # Accept both decimal (MB) and binary (MiB) units; fall back to raw bytes when no unit is present.
    units = {
        "b": 1,
        "kb": 1000, "k": 1000,
        "mb": 1000**2, "m": 1000**2,
        "gb": 1000**3, "g": 1000**3,
        "kib": 1024, "mib": 1024**2, "gib": 1024**3,
    }
    for u, mult in units.items():
        if s.endswith(u):
            val = float(s[: -len(u)])
            return int(val * mult)
    # No unit provided: interpret as raw bytes.
    return int(s)


def is_probably_binary(path: Path, sample_bytes: int = 4096) -> bool:
    """
    Simple heuristic: binary if it contains a NUL byte or cannot be decoded.
    """
    try:
        with path.open("rb") as f:
            chunk = f.read(sample_bytes)
        if b"\x00" in chunk:
            return True
        # Try a tolerant UTF-8 decode; failure implies likely binary.
        chunk.decode("utf-8")
        return False
    except Exception:
        # If we cannot read or decode, be conservative and treat it as binary.
        return True


def read_text_best_effort(path: Path, normalize_eol: bool) -> str:
    """
    Best-effort text read: try UTF-8 then Latin-1. Normalize EOL when requested.
    """
    data = None
    try:
        data = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        data = path.read_text(encoding="latin-1")
    # Optionally normalize Windows/Mac newlines to Unix for more stable diffs.
    if normalize_eol:
        data = data.replace("\r\n", "\n").replace("\r", "\n")
    return data


def file_bytes_equal(p1: Path, p2: Path) -> bool:
    """
    Compare file contents via hash (fast enough for most cases).
    """

    def _hash(p: Path) -> str:
        # Stream file content through SHA-256 to avoid loading large files into memory.
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    return _hash(p1) == _hash(p2)


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def avoid_collision(path: Path) -> Path:
    """
    Avoid name collisions in the output directory by appending a numeric suffix when needed.
    Example: "file.txt.modified" -> "file.txt.modified (1)"
    """
    if not path.exists():
        return path
    base = path
    n = 1
    while True:
        candidate = Path(f"{base} ({n})")
        if not candidate.exists():
            return candidate
        n += 1


def rel_parts_with_deleted_suffix(rel: Path) -> Path:
    """
    Append ".deleted" to every part of a relative path (directory names only).
    Example: "dir/sub" -> "dir.deleted/sub.deleted"
    """
    parts = list(rel.parts)
    if not parts:
        return rel
    new_parts = [p + ".deleted" for p in parts]
    return Path(*new_parts)
