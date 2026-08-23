"""
Core ToolManager coordinator for eSim EDA tool orchestration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from esim_tool_manager.detector import SystemDetector
from esim_tool_manager.exceptions import (
    InvalidToolNameError,
    ToolNotFoundError,
)
from esim_tool_manager.installer import PackageInstaller
from esim_tool_manager.logger import get_logger
from esim_tool_manager.models import (
    InstallationResult,
    StatusEnum,
    SystemInfo,
    ToolDefinition,
    ToolStatus,
)
from esim_tool_manager.tools import (
    get_all_tools,
    get_tool,
    is_tool_registered,
)

logger = get_logger("esim_manager.core")


class ToolManager:
    """High-level facade coordinating tool detection, inspection, and installation."""

    def __init__(self) -> None:
        self.detector = SystemDetector()
        self.installer = PackageInstaller()

    def get_system_info(self) -> SystemInfo:
        """Query and return host system environment details."""
        return self.detector.get_system_info()

    def list_supported_tools(self) -> list[ToolDefinition]:
        """Return all supported external tool specifications."""
        return get_all_tools()

    def check_all_dependencies(self, custom_paths: list[Path] | None = None) -> list[ToolStatus]:
        """Audit status and versions of all supported external tools."""
        logger.info("Executing comprehensive dependency check across all tools.")
        tools = self.list_supported_tools()
        results: list[ToolStatus] = []
        for tool in tools:
            status = self.detector.check_tool(tool, custom_paths=custom_paths)
            results.append(status)
        return results

    def check_single_tool(self, tool_name: str, custom_paths: list[Path] | None = None) -> ToolStatus:
        """Audit status and version of a specific named tool."""
        tool = get_tool(tool_name)
        return self.detector.check_tool(tool, custom_paths=custom_paths)

    def get_tool_version(self, tool_name: str) -> ToolStatus:
        """Retrieve installed version information for a tool."""
        return self.check_single_tool(tool_name)

    def get_tool_info(self, tool_name: str) -> ToolDefinition:
        """Fetch metadata definition for a tool."""
        return get_tool(tool_name)

    def install_tool(
        self,
        tool_name: str,
        package_manager: str | None = None,
        dry_run: bool = False,
        non_interactive: bool = True,
    ) -> InstallationResult:
        """Install a tool via platform package manager."""
        logger.info(f"Initiating installation request for tool '{tool_name}' (dry_run={dry_run})")
        tool = get_tool(tool_name)
        return self.installer.install(
            tool=tool,
            strategy_name=package_manager,
            dry_run=dry_run,
            non_interactive=non_interactive,
        )

    def run_doctor(self) -> dict[str, Any]:
        """
        Execute comprehensive system diagnostic.
        Returns detailed dictionary containing system info, tool statuses, and recommendations.
        """
        logger.info("Running eSim Doctor diagnostics.")
        sys_info = self.get_system_info()
        statuses = self.check_all_dependencies()

        installed_count = sum(1 for s in statuses if s.status == StatusEnum.INSTALLED)
        missing_count = sum(1 for s in statuses if s.status == StatusEnum.MISSING)
        incompatible_count = sum(1 for s in statuses if s.status == StatusEnum.INCOMPATIBLE)
        unknown_count = sum(1 for s in statuses if s.status == StatusEnum.UNKNOWN)

        recommendations: list[str] = []

        for status in statuses:
            if status.status == StatusEnum.MISSING:
                recommendations.append(
                    f"Install missing dependency '{status.display_name}' via: "
                    f"esim-manager install {status.name}"
                )
            elif status.status == StatusEnum.INCOMPATIBLE:
                recommendations.append(
                    f"Upgrade '{status.display_name}' (currently {status.installed_version}) "
                    f"to at least {status.required_version}."
                )

        if not sys_info.available_package_managers:
            recommendations.append(
                "No standard package manager detected. You may need to manually install software dependencies."
            )

        return {
            "system_info": sys_info,
            "tool_statuses": statuses,
            "summary": {
                "total": len(statuses),
                "installed": installed_count,
                "missing": missing_count,
                "incompatible": incompatible_count,
                "unknown": unknown_count,
                "healthy": (missing_count == 0 and incompatible_count == 0),
            },
            "recommendations": recommendations,
        }
