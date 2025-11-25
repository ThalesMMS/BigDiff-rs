# BigDiff

**BigDiff** is a cross-platform Python tool to compare two directory trees and generate a third one containing only the differences, in a human-readable and auditable way.

It is useful when you need to track new files, deletions, modifications, or even line-by-line changes with annotations that respect the comment syntax of each file type.

---

## Features

- Compares **folder1** (base) and **folder2** (target), producing **folder3** (output).
- **Unchanged files** are omitted from the output.
- **New files** are copied with `.new` suffix.
- **Deleted files** are copied with `.deleted` suffix.
- **Deleted directories** appear with `.deleted` suffix, including their contents.
- **Modified files**:
  - Copied with `.modified` suffix.
  - Line-level diff is embedded directly in the file:
    - Deleted lines are commented with `DELETED`.
    - Added lines are preserved with `NEW` annotation.
    - Unchanged lines remain unchanged for context.
  - Comment syntax matches file type (`#`, `//`, `/* */`, `<!-- -->`, etc).
- **Binary or oversized files**:
  - Copied directly with `.modified` suffix.
  - An extra `.NOTE.txt` file explains that line-level diff was skipped.

---

## Installation

Clone this repository (Python 3.8+):

```bash
git clone https://github.com/your-username/bigdiff.git
cd bigdiff
python -m bigdiff --help
```

The CLI wrapper `bigdiff.py` remains available for backwards compatibility, but the project is now a proper package so you can run `python -m bigdiff` or import it as a library.

---

## Usage

```bash
python -m bigdiff FOLDER1 FOLDER2 FOLDER3 [options]
# or, for compatibility:
python bigdiff.py FOLDER1 FOLDER2 FOLDER3 [options]
```

### Examples

```bash
# Basic comparison
python bigdiff.py ./before ./after ./diff_out

# Normalize line endings and ignore temporary files
python bigdiff.py ./a ./b ./out --normalize-eol --ignore ".git,__pycache__,*.log"

# Dry-run (does not write, only shows the plan)
python bigdiff.py ./a ./b ./out --dry-run
```

---

## Options

- `--ignore, -i` : glob patterns to ignore (repeatable or comma-separated).
- `--normalize-eol, -E` : normalize CRLF/LF before comparing text.
- `--max-text-size, -S` : maximum size for text diff (default `5MB`).
- `--dry-run` : only show what would be done, no output written.

---

## Library Usage

You can also call BigDiff programmatically:

```python
from pathlib import Path

from bigdiff import Options, bigdiff, parse_size

opts = Options(
    normalize_eol=True,
    max_text_size=parse_size("5MB"),
    ignore_patterns=[],
    dry_run=False,
)
counters = bigdiff(Path("./before"), Path("./after"), Path("./diff_out"), opts)
print(counters)
```

---

## Example Output

If `example.py` was modified:

```diff
# DELETED: print("Hello World")
print("New line added")  # NEW
```

If `config.ini` was removed:

```
config.ini.deleted
```

If `notes.txt` was created:

```
notes.txt.new
```

---

## Internal Strategy

- Comparison by **SHA-256 hash** (fast and safe).
- Text diff via `difflib.ndiff`.
- Simple heuristics to detect binary files.
- Collision avoidance in output (creates `file (1).modified`, etc).
- Ensures output folder is never inside input folders.

---

## Future Improvements

- JSON report with statistics.
- Parallel processing for large datasets.
- Rename detection (`delete+new` to `rename`).
- Plugins for binary formats (e.g., DICOM, medical imaging).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

Thales Matheus Mendonça Santos
