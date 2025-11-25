#
# __main__.py
# BigDiff
#
# Entry module to allow `python -m bigdiff` execution by delegating to the CLI main function.
#
# Thales Matheus Mendonça Santos - November 2025
from __future__ import annotations

import sys

from .cli import main


if __name__ == "__main__":
    # Delegate to the CLI implementation so module execution and script execution behave the same.
    sys.exit(main())
