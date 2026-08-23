"""
Git version control definition for eSim.
"""

from __future__ import annotations

from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools.base import BaseToolProvider


class GitTool(BaseToolProvider):
    """Git version control provider."""

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="git",
            display_name="Git Version Control",
            description="Distributed version control system for project repositories and schematic libraries.",
            executable="git",
            alternate_executables=[],
            minimum_version="2.20.0",
            version_command=["--version"],
            version_regex=r"git version\s+(\d+(?:\.\d+)+)",
            package_names={
                "apt": "git",
                "apt-get": "git",
                "brew": "git",
                "winget": "Git.Git",
                "pacman": "git",
                "dnf": "git",
                "choco": "git",
            },
            supported_platforms=["linux", "windows", "darwin"],
            category="Version Control",
            docs_url="https://git-scm.com",
        )
