"""
Python runtime definition for eSim.
"""

from __future__ import annotations

from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools.base import BaseToolProvider


class PythonTool(BaseToolProvider):
    """Python 3 runtime environment provider."""

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="python",
            display_name="Python Runtime",
            description="Python 3 programming environment for eSim orchestration and subcircuit generation.",
            executable="python3",
            alternate_executables=["python", "python3.10", "python3.11", "python3.12"],
            minimum_version="3.10.0",
            version_command=["--version"],
            version_regex=r"Python\s+(\d+(?:\.\d+)+)",
            package_names={
                "apt": "python3",
                "apt-get": "python3",
                "brew": "python@3.12",
                "winget": "Python.Python.3.12",
                "pacman": "python",
                "dnf": "python3",
                "choco": "python3",
            },
            supported_platforms=["linux", "windows", "darwin"],
            category="Core Runtime",
            docs_url="https://www.python.org",
        )
