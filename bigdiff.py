#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# bigdiff.py
# BigDiff
#
# Compatibility wrapper that forwards execution to the CLI entrypoint for module/script parity.
#
# Thales Matheus Mendonça Santos - November 2025
"""
Compatibility wrapper for the BigDiff CLI.
Prefer `python -m bigdiff` or importing `bigdiff` as a package.
"""

import sys

from bigdiff.cli import main


if __name__ == "__main__":
    # Compatibility wrapper so invoking this file mirrors `python -m bigdiff`.
    sys.exit(main())
