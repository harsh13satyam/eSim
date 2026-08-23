"""
Data models and typed representations for eSim Tool Manager.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable


class StatusEnum(str, Enum):
    """Status classification for tools."""
    INSTALLED = "INSTALLED"
    MISSING = "MISSING"
    INCOMPATIBLE = "INCOMPATIBLE"
    UNKNOWN = "UNKNOWN"
    UNSUPPORTED = "UNSUPPORTED"

    @property
    def symbol(self) -> str:
        if self == StatusEnum.INSTALLED:
            return "✓"
        if self == StatusEnum.MISSING:
            return "✗"
        if self == StatusEnum.INCOMPATIBLE:
            return "!"
        if self == StatusEnum.UNSUPPORTED:
            return "⊘"
        return "?"

    @property
    def label(self) -> str:
        return f"[{self.value}]"


@dataclass(frozen=True)
class SystemInfo:
    """Represents detected host operating system and execution environment."""
    os_type: str  # linux, windows, darwin
    os_name: str  # e.g., Ubuntu, Windows 11, macOS Monterey
    os_version: str  # e.g., 22.04, 10.0.22621
    architecture: str  # e.g., x86_64, aarch64, AMD64
    python_version: str
    is_admin: bool
    available_package_managers: tuple[str, ...] = field(default_factory=tuple)
    hostname: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "os_type": self.os_type,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "architecture": self.architecture,
            "python_version": self.python_version,
            "is_admin": self.is_admin,
            "available_package_managers": list(self.available_package_managers),
            "hostname": self.hostname,
        }


@dataclass
class ToolDefinition:
    """Specification of an external tool supported by eSim."""
    name: str  # Canonical identifier (e.g. 'ngspice', 'kicad')
    display_name: str  # Human readable name (e.g. 'Ngspice', 'KiCad EDA')
    description: str
    executable: str  # Primary binary name (e.g. 'ngspice')
    alternate_executables: list[str] = field(default_factory=list)
    minimum_version: str = "0.0.0"
    version_command: list[str] = field(default_factory=lambda: ["--version"])
    version_regex: str = r"(\d+(?:\.\d+)+(?:[a-zA-Z0-9_\-\.]*))"
    package_names: dict[str, str] = field(default_factory=dict)
    # package_names mapping, e.g.:
    # {"apt": "ngspice", "winget": "Ngspice.Ngspice", "brew": "libngspice", "pacman": "ngspice", "dnf": "ngspice"}
    supported_platforms: list[str] = field(default_factory=lambda: ["linux", "windows", "darwin"])
    category: str = "EDA Simulator"
    docs_url: str = ""
    custom_version_extractor: Callable[[str, str], str | None] | None = None
    custom_install_instructions: dict[str, str] = field(default_factory=dict)

    def get_package_for_manager(self, package_manager: str) -> str | None:
        """Retrieve package identifier for a specific package manager."""
        return self.package_names.get(package_manager)

    def is_platform_supported(self, platform_name: str) -> bool:
        """Check if tool is supported on the given platform."""
        return platform_name.lower() in [p.lower() for p in self.supported_platforms]


@dataclass
class ToolStatus:
    """Detailed runtime status of a tool on the host system."""
    tool: ToolDefinition
    status: StatusEnum
    installed_version: str | None = None
    required_version: str = "0.0.0"
    executable_path: Path | None = None
    message: str = ""
    raw_version_output: str = ""

    @property
    def name(self) -> str:
        return self.tool.name

    @property
    def display_name(self) -> str:
        return self.tool.display_name

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.tool.name,
            "display_name": self.tool.display_name,
            "status": self.status.value,
            "symbol": self.status.symbol,
            "installed_version": self.installed_version,
            "required_version": self.required_version,
            "executable_path": str(self.executable_path) if self.executable_path else None,
            "message": self.message,
            "category": self.tool.category,
        }


@dataclass
class InstallationResult:
    """Result of an installation or dry-run execution."""
    success: bool
    tool_name: str
    package_manager: str | None
    command_executed: list[str] = field(default_factory=list)
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""
    message: str = ""
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "tool_name": self.tool_name,
            "package_manager": self.package_manager,
            "command_executed": self.command_executed,
            "return_code": self.return_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "message": self.message,
            "dry_run": self.dry_run,
        }


@dataclass(frozen=True)
class VersionComparisonResult:
    """Outcome of comparing installed vs minimum required version."""
    installed_version: str
    required_version: str
    satisfies: bool
    details: str = ""
