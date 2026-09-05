#!/usr/bin/env python3
"""Compatibility wrapper; use arabic_mechanical_lint.py in v1.1+."""
from arabic_mechanical_lint import *  # noqa: F401,F403
if __name__ == "__main__":
    from arabic_mechanical_lint import main
    raise SystemExit(main())
