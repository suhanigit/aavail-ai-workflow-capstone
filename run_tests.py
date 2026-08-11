#!/usr/bin/env python3
"""Run every unit test with one command."""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(root / "tests")],
        cwd=root,
    )
    raise SystemExit(result.returncode)
