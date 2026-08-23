"""
System and dependency detection engine for eSim Tool Manager.
Discovers tools, analyzes binaries, verifies versions, and audits OS capabilities.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from esim_tool_manager.logger import get_logger
from esim_tool_manager.models import (
    StatusEnum,
    SystemInfo,
    ToolDefinition,
    ToolStatus,
)
from esim_tool_manager.platform import PlatformManager
from esim_tool_manager.version_checker import VersionChecker

logger = get_logger("esim_manager.detector")


class SystemDetector:
    """Discovers host operating system features and inspects installed EDA tools."""

    PACKAGE_MANAGERS = (
        "apt-get",
        "apt",
        "pacman",
        "dnf",
        "zypper",
        "brew",
        "winget",
        "choco",
        "scoop",
    )

    @classmethod
    def get_system_info(cls) -> SystemInfo:
        """Collect host system metadata and detected package managers."""
        os_type = PlatformManager.get_os_type()
        os_name, os_version = PlatformManager.get_os_name_and_version()
        arch = PlatformManager.get_architecture()
        is_admin = PlatformManager.is_admin()
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # Probe available package managers
        available_pms: list[str] = []
        for pm in cls.PACKAGE_MANAGERS:
            if shutil.which(pm):
                # Standardize 'apt-get' to 'apt' in priority if both exist
                if pm == "apt-get" and "apt" in available_pms:
                    continue
                available_pms.append(pm)

        import socket
        try:
            hostname = socket.gethostname()
        except Exception:
            hostname = "localhost"

        info = SystemInfo(
            os_type=os_type,
            os_name=os_name,
            os_version=os_version,
            architecture=arch,
            python_version=py_ver,
            is_admin=is_admin,
            available_package_managers=tuple(available_pms),
            hostname=hostname,
        )
        logger.debug(f"Detected system info: {info}")
        return info

    @classmethod
    def check_tool(cls, tool: ToolDefinition, custom_paths: list[Path] | None = None) -> ToolStatus:
        """
        Check whether a specific tool is installed, accessible, and meets version requirements.
        Safely executes the tool's version command without invoking shell.
        """
        logger.info(f"Checking status for tool: {tool.name} ({tool.display_name})")

        # 1. Verify platform compatibility
        current_os = PlatformManager.get_os_type()
        if not tool.is_platform_supported(current_os):
            msg = f"{tool.display_name} is not supported on platform '{current_os}'."
            logger.warning(msg)
            return ToolStatus(
                tool=tool,
                status=StatusEnum.UNSUPPORTED,
                required_version=tool.minimum_version,
                message=msg,
            )

        # 2. Locate binary on system
        candidate_names = [tool.executable] + tool.alternate_executables
        exec_path: Path | None = None

        for name in candidate_names:
            exec_path = PlatformManager.find_executable(name, custom_paths=custom_paths)
            if exec_path:
                break

        if not exec_path:
            msg = f"Binary '{tool.executable}' not found on PATH or standard directories."
            logger.info(f"{tool.name}: MISSING ({msg})")
            return ToolStatus(
                tool=tool,
                status=StatusEnum.MISSING,
                required_version=tool.minimum_version,
                message=msg,
            )

        # 3. Query tool version
        # Special case: if tool is python and we are running inside python, we can also check directly
        version_output = ""
        version_extracted: str | None = None

        cmd = [str(exec_path)] + tool.version_command
        try:
            # Execute safely with timeout and shell=False
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            # Combine stdout and stderr (many EDA tools print version or banner to stderr)
            version_output = (res.stdout or "") + "\n" + (res.stderr or "")

            if tool.custom_version_extractor:
                version_extracted = tool.custom_version_extractor(res.stdout, res.stderr)
            else:
                version_extracted = VersionChecker.extract_version(
                    version_output,
                    regex_pattern=tool.version_regex,
                )

        except subprocess.TimeoutExpired:
            msg = f"Timed out while retrieving version from '{exec_path}'."
            logger.error(msg)
            return ToolStatus(
                tool=tool,
                status=StatusEnum.UNKNOWN,
                executable_path=exec_path,
                required_version=tool.minimum_version,
                message=msg,
            )
        except (PermissionError, OSError) as err:
            msg = f"Permission or execution error running '{exec_path}': {err}"
            logger.error(msg)
            return ToolStatus(
                tool=tool,
                status=StatusEnum.UNKNOWN,
                executable_path=exec_path,
                required_version=tool.minimum_version,
                message=msg,
            )

        if not version_extracted:
            msg = f"Executable found at '{exec_path}', but failed to parse version string."
            logger.warning(msg)
            return ToolStatus(
                tool=tool,
                status=StatusEnum.UNKNOWN,
                executable_path=exec_path,
                required_version=tool.minimum_version,
                message=msg,
                raw_version_output=version_output.strip(),
            )

        # 4. Compare installed version vs required version
        comp = VersionChecker.compare(version_extracted, tool.minimum_version)
        if comp.satisfies:
            msg = f"Version {version_extracted} meets minimum requirement {tool.minimum_version}."
            logger.info(f"{tool.name}: INSTALLED ({version_extracted}) at {exec_path}")
            return ToolStatus(
                tool=tool,
                status=StatusEnum.INSTALLED,
                installed_version=version_extracted,
                required_version=tool.minimum_version,
                executable_path=exec_path,
                message=msg,
                raw_version_output=version_output.strip(),
            )
        else:
            msg = f"Version {version_extracted} is below required minimum {tool.minimum_version}."
            logger.warning(f"{tool.name}: INCOMPATIBLE ({msg})")
            return ToolStatus(
                tool=tool,
                status=StatusEnum.INCOMPATIBLE,
                installed_version=version_extracted,
                required_version=tool.minimum_version,
                executable_path=exec_path,
                message=msg,
                raw_version_output=version_output.strip(),
            )
