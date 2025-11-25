#
# comment_styles.py
# BigDiff
#
# Defines how NEW/DELETED markers are injected for different file types via line or block comment styles.
#
# Thales Matheus Mendonça Santos - November 2025
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommentStyle:
    """
    Defines how to annotate NEW/DELETED markers for a file.
    - deleted_line(s: str) -> str: returns the commented representation of a deleted line.
    - append_new_suffix(s: str) -> str: appends a NEW suffix to a line before its trailing newline.
    """

    name: str

    def deleted_line(self, line: str) -> str:
        raise NotImplementedError

    def append_new_suffix(self, line: str) -> str:
        raise NotImplementedError


class LinePrefixStyle(CommentStyle):
    """
    Classic single-line comment style such as "# " or "// ".
    Deletion: "# DELETED: <content>\\n"
    New:      "<content>  # NEW\\n"
    """

    def __init__(self, name: str, line_prefix: str, new_suffix: str) -> None:
        super().__init__(name=name)
        self._prefix = line_prefix
        self._new_suffix = new_suffix

    def deleted_line(self, line: str) -> str:
        # Preserve existing trailing newline so we do not collapse paragraphs.
        if line.endswith("\n"):
            content = line[:-1]
            end = "\n"
        else:
            content = line
            end = ""
        return f"{self._prefix}DELETED: {content}{end}"

    def append_new_suffix(self, line: str) -> str:
        # Attach the NEW marker before the final newline (if present).
        if line.endswith("\n"):
            content = line[:-1]
            end = "\n"
        else:
            content = line
            end = ""
        return f"{content}{self._new_suffix}{end}"


class BlockStyle(CommentStyle):
    """
    Block comment style like "/* ... */" or "<!-- ... -->".
    Deletion: "/* DELETED: <content> */\\n"
    New:      "<content>  /* NEW */\\n"
    """

    def __init__(self, name: str, open_mark: str, close_mark: str, new_block: str) -> None:
        super().__init__(name=name)
        self._open = open_mark
        self._close = close_mark
        self._new_block = new_block

    def deleted_line(self, line: str) -> str:
        # Wrap deleted content in the chosen block markers.
        if line.endswith("\n"):
            content = line[:-1]
            end = "\n"
        else:
            content = line
            end = ""
        return f"{self._open} DELETED: {content} {self._close}{end}"

    def append_new_suffix(self, line: str) -> str:
        # Add a block-level NEW marker but keep the line payload intact.
        if line.endswith("\n"):
            content = line[:-1]
            end = "\n"
        else:
            content = line
            end = ""
        return f"{content} {self._new_block}{end}"


def comment_style_for(path: Path) -> CommentStyle:
    ext = path.suffix.lower()

    # Line-prefix styles (single-line comment markers)
    slash_exts = {".c", ".h", ".cpp", ".hpp", ".cc", ".java", ".js", ".ts", ".tsx",
                  ".cs", ".swift", ".go", ".kt", ".kts", ".scala", ".dart", ".php", ".rs"}
    hash_exts = {".py", ".sh", ".rb", ".r", ".ps1", ".toml", ".yaml", ".yml", ".cfg"}
    dash_exts = {".sql", ".hs"}  # "-- "
    percent_exts = {".tex", ".m"}  # Note: .m might be MATLAB (%), not ObjC
    semicolon_exts = {".ini"}
    csv_like = {".csv", ".tsv"}
    text_like = {".txt", ".log", ".cfg", ".conf"}

    # Block comment styles
    html_exts = {".html", ".htm", ".xml", ".xhtml", ".svg", ".md"}  # For Markdown we also use <!-- -->
    cblock_exts = {".css", ".scss", ".less"}
    json_exts = {".json"}  # Use /* */ even if strict JSON does not allow comments

    if ext in slash_exts:
        return LinePrefixStyle("slash", "// ", " // NEW")
    if ext in hash_exts or ext in text_like:
        return LinePrefixStyle("hash", "# ", " # NEW")
    if ext in dash_exts:
        return LinePrefixStyle("dash", "-- ", " -- NEW")
    if ext in percent_exts:
        return LinePrefixStyle("percent", "% ", " % NEW")
    if ext in semicolon_exts:
        return LinePrefixStyle("semicolon", "; ", " ; NEW")
    if ext in csv_like:
        return LinePrefixStyle("csv", "# ", " # NEW")  # Safe comment symbol when kept off data rows

    if ext in html_exts:
        return BlockStyle("html", "<!--", "-->", "<!-- NEW -->")
    if ext in cblock_exts or ext in json_exts:
        return BlockStyle("cblock", "/*", "*/", "/* NEW */")

    # Safe and readable fallback when we do not recognize the extension.
    return LinePrefixStyle("fallback", "# ", " # NEW")
