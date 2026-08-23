#!/usr/bin/env python3
"""
eSim Automated Tool Manager — Main Entrypoint.
Enables direct invocation from project root via:
    python main.py <command>
"""

import sys
from pathlib import Path

# Add src to sys.path if running as a script from repository root
REPO_SRC = Path(__file__).resolve().parent / "src"
if str(REPO_SRC) not in sys.path:
    sys.path.insert(0, str(REPO_SRC))

from esim_tool_manager.cli import main

if __name__ == "__main__":
    sys.exit(main())
