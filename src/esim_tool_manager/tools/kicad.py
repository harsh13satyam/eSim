"""
KiCad Electronic Design Automation suite definition for eSim.
"""

from __future__ import annotations

import re
from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools.base import BaseToolProvider


def extract_kicad_version(stdout: str, stderr: str) -> str | None:
    """Custom extractor for KiCad and kicad-cli output."""
    combined = (stdout or "") + "\n" + (stderr or "")
    patterns = [
        r"(?:kicad|version|release|v)?\s*\(?(\d+\.\d+(?:\.\d+)?(?:-[0-9a-zA-Z]+)?)",
        r"(\d+\.\d+\.\d+)",
        r"(\d+\.\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, combined, re.IGNORECASE)
        if m:
            # clean parentheses or trailing characters
            return m.group(1).strip("()").split("-")[0]
    return None


class KiCadTool(BaseToolProvider):
    """KiCad EDA suite provider."""

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="kicad",
            display_name="KiCad EDA Suite",
            description="Comprehensive electronic schematic capture and PCB layout design system for eSim.",
            executable="kicad",
            alternate_executables=["kicad-cli", "eeschema", "kicad.exe"],
            minimum_version="7.0.0",
            version_command=["--version"],
            version_regex=r"(?:kicad|version)?\s*\(?(\d+(?:\.\d+)+)",
            package_names={
                "apt": "kicad",
                "apt-get": "kicad",
                "brew": "kicad",
                "winget": "KiCad.KiCad",
                "pacman": "kicad",
                "dnf": "kicad",
                "choco": "kicad",
            },
            supported_platforms=["linux", "windows", "darwin"],
            category="Schematic & PCB Design",
            docs_url="https://www.kicad.org",
            custom_version_extractor=extract_kicad_version,
            custom_install_instructions={
                "linux": "sudo add-apt-repository --yes ppa:kicad/kicad-7.0-releases && sudo apt-get update && sudo apt-get install --yes kicad",
                "windows": "winget install KiCad.KiCad",
                "darwin": "brew install --cask kicad",
            },
        )
