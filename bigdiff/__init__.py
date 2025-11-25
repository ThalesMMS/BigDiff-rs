#
# __init__.py
# BigDiff
#
# Exposes the public API surface so BigDiff can be used as a library in addition to the CLI tools.
#
# Thales Matheus Mendonça Santos - November 2025
from __future__ import annotations

from .cli import main, parse_args
from .comment_styles import BlockStyle, CommentStyle, LinePrefixStyle, comment_style_for
from .core import Counters, Options, annotate_text_diff, bigdiff, is_parent
from .io_utils import (
    avoid_collision,
    ensure_parent_dir,
    file_bytes_equal,
    is_probably_binary,
    parse_size,
    read_text_best_effort,
    rel_parts_with_deleted_suffix,
)
from .scanner import DEFAULT_IGNORES, ScanResult, is_ignored, scan_dir

# Expose a convenience surface so users can import BigDiff as a library or call the CLI helpers.
__all__ = [
    "BlockStyle",
    "CommentStyle",
    "LinePrefixStyle",
    "comment_style_for",
    "Counters",
    "Options",
    "annotate_text_diff",
    "bigdiff",
    "is_parent",
    "main",
    "parse_args",
    "avoid_collision",
    "ensure_parent_dir",
    "file_bytes_equal",
    "is_probably_binary",
    "parse_size",
    "read_text_best_effort",
    "rel_parts_with_deleted_suffix",
    "DEFAULT_IGNORES",
    "ScanResult",
    "is_ignored",
    "scan_dir",
]
