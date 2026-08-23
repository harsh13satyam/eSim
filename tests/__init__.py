"""
eSim Tool Manager Unit Test Suite.
"""

import sys
from pathlib import Path

# Automatically ensure 'src' is in sys.path for test discovery
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
