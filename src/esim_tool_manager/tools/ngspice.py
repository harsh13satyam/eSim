"""
Ngspice simulation engine definition for eSim.
"""

from __future__ import annotations

import re
from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools.base import BaseToolProvider


def extract_ngspice_version(stdout: str, stderr: str) -> str | None:
    """Custom extractor for ngspice banner output."""
    combined = (stdout or "") + "\n" + (stderr or "")
    # Match patterns like "** ngspice-42.2 :", "ngspice-38", "ngspice version 42"
    patterns = [
        r"ngspice-(\d+(?:\.\d+)*)",
        r"ngspice\s+version\s+(\d+(?:\.\d+)*)",
        r"ngspice\s*:\s*(\d+(?:\.\d+)*)",
        r"(\d+(?:\.\d+)+)",
    ]
    for pat in patterns:
        m = re.search(pat, combined, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(".")
    return None


class NgspiceTool(BaseToolProvider):
    """Ngspice circuit simulation engine provider."""

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="ngspice",
            display_name="Ngspice Circuit Simulator",
            description="General-purpose circuit simulator for linear and non-linear DC, transient, and AC analyses in eSim.",
            executable="ngspice",
            alternate_executables=["ngspice.exe"],
            minimum_version="38.0.0",
            version_command=["-v"],
            version_regex=r"(?:ngspice[- ]|version\s*)(\d+(?:\.\d+)*)",
            package_names={
                "apt": "ngspice",
                "apt-get": "ngspice",
                "brew": "libngspice",
                "winget": "Ngspice.Ngspice",
                "pacman": "ngspice",
                "dnf": "ngspice",
                "choco": "ngspice",
            },
            supported_platforms=["linux", "windows", "darwin"],
            category="Circuit Simulation",
            docs_url="https://ngspice.sourceforge.io",
            custom_version_extractor=extract_ngspice_version,
            custom_install_instructions={
                "linux": "sudo apt-get install ngspice",
                "windows": "winget install Ngspice.Ngspice",
                "darwin": "brew install libngspice",
            },
        )
