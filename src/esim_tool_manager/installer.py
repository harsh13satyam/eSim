"""
Cross-platform package installer subsystem for eSim Tool Manager.
Implements modular package manager strategies with privilege checks, dry-run modes,
and secure parameter-array execution without shell invocation.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import ClassVar

from esim_tool_manager.exceptions import (
    InstallationError,
    InsufficientPrivilegesError,
    UnsupportedPlatformError,
)
from esim_tool_manager.logger import get_logger
from esim_tool_manager.models import InstallationResult, ToolDefinition
from esim_tool_manager.platform import PlatformManager

logger = get_logger("esim_manager.installer")


class BaseInstallerStrategy(ABC):
    """Abstract base strategy for a specific host package manager."""

    name: ClassVar[str] = "base"

    @classmethod
    def is_available(cls) -> bool:
        """Return True if the package manager binary exists on system PATH."""
        return shutil.which(cls.name) is not None or (
            cls.name == "apt" and shutil.which("apt-get") is not None
        )

    @classmethod
    def requires_elevation(cls) -> bool:
        """Return True if package installation commands typically require root/admin privileges."""
        return True

    @abstractmethod
    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        """Generate the argument array for the installation command."""
        raise NotImplementedError

    def execute_install(
        self,
        tool: ToolDefinition,
        dry_run: bool = False,
        non_interactive: bool = True,
        timeout: int = 300,
    ) -> InstallationResult:
        """
        Execute package installation using this strategy.
        Safely executes via subprocess without shell=True.
        """
        pkg = tool.get_package_for_manager(self.name)
        if not pkg:
            # Check fallback name or tool executable
            pkg = tool.name

        cmd = self.build_install_command(pkg, non_interactive=non_interactive)
        cmd_str = " ".join(cmd)

        logger.info(f"Preparing installation for '{tool.name}' via {self.name}: {cmd_str}")

        if dry_run:
            msg = f"[DRY RUN] Would execute command: '{cmd_str}'"
            logger.info(msg)
            return InstallationResult(
                success=True,
                tool_name=tool.name,
                package_manager=self.name,
                command_executed=cmd,
                return_code=0,
                stdout="Dry-run simulation succeeded.",
                stderr="",
                message=msg,
                dry_run=True,
            )

        # Check privilege requirements
        is_admin = PlatformManager.is_admin()
        if self.requires_elevation() and not is_admin:
            # If not root on Linux/Unix, check if sudo is in the command or if elevation is needed
            if cmd[0] != "sudo" and shutil.which("sudo"):
                cmd.insert(0, "sudo")
                cmd_str = " ".join(cmd)
            elif not shutil.which("sudo") and not is_admin:
                msg = (
                    f"Installation via {self.name} requires root/administrator privileges, "
                    "but current user does not have elevated rights and 'sudo' is unavailable."
                )
                logger.error(msg)
                return InstallationResult(
                    success=False,
                    tool_name=tool.name,
                    package_manager=self.name,
                    command_executed=cmd,
                    return_code=1,
                    stdout="",
                    stderr=msg,
                    message=msg,
                    dry_run=False,
                )

        try:
            logger.info(f"Running installation subprocess: {cmd}")
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            success = (proc.returncode == 0)
            if success:
                msg = f"Successfully installed '{tool.display_name}' via {self.name}."
                logger.info(msg)
            else:
                msg = f"Installation command failed with exit code {proc.returncode}."
                logger.error(f"{msg}\nSTDERR: {proc.stderr}\nSTDOUT: {proc.stdout}")

            return InstallationResult(
                success=success,
                tool_name=tool.name,
                package_manager=self.name,
                command_executed=cmd,
                return_code=proc.returncode,
                stdout=proc.stdout or "",
                stderr=proc.stderr or "",
                message=msg,
                dry_run=False,
            )

        except subprocess.TimeoutExpired:
            msg = f"Installation command timed out after {timeout} seconds."
            logger.error(msg)
            return InstallationResult(
                success=False,
                tool_name=tool.name,
                package_manager=self.name,
                command_executed=cmd,
                return_code=-1,
                stdout="",
                stderr=msg,
                message=msg,
                dry_run=False,
            )
        except (PermissionError, OSError) as err:
            msg = f"Failed to invoke installation command '{cmd_str}': {err}"
            logger.error(msg)
            return InstallationResult(
                success=False,
                tool_name=tool.name,
                package_manager=self.name,
                command_executed=cmd,
                return_code=-1,
                stdout="",
                stderr=str(err),
                message=msg,
                dry_run=False,
            )


class AptStrategy(BaseInstallerStrategy):
    """Debian/Ubuntu Advanced Package Tool (apt / apt-get) strategy."""

    name: ClassVar[str] = "apt"

    @classmethod
    def is_available(cls) -> bool:
        return shutil.which("apt-get") is not None or shutil.which("apt") is not None

    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        binary = "apt-get" if shutil.which("apt-get") else "apt"
        cmd = [binary, "install"]
        if non_interactive:
            cmd.append("-y")
        cmd.append(package_name)
        return cmd


class PacmanStrategy(BaseInstallerStrategy):
    """Arch Linux package manager (pacman) strategy."""

    name: ClassVar[str] = "pacman"

    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        cmd = ["pacman", "-S"]
        if non_interactive:
            cmd.append("--noconfirm")
        cmd.append(package_name)
        return cmd


class DnfStrategy(BaseInstallerStrategy):
    """Fedora / RHEL DNF package manager strategy."""

    name: ClassVar[str] = "dnf"

    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        cmd = ["dnf", "install"]
        if non_interactive:
            cmd.append("-y")
        cmd.append(package_name)
        return cmd


class BrewStrategy(BaseInstallerStrategy):
    """macOS / Linux Homebrew strategy."""

    name: ClassVar[str] = "brew"

    @classmethod
    def requires_elevation(cls) -> bool:
        # Homebrew explicitly forbids running as root
        return False

    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        cmd = ["brew", "install", package_name]
        return cmd


class WingetStrategy(BaseInstallerStrategy):
    """Microsoft Windows Package Manager (winget) strategy."""

    name: ClassVar[str] = "winget"

    @classmethod
    def requires_elevation(cls) -> bool:
        return False

    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        cmd = ["winget", "install", "--exact", "--id", package_name]
        if non_interactive:
            cmd.extend([
                "--accept-source-agreements",
                "--accept-package-agreements",
                "--disable-interactivity",
            ])
        return cmd


class ChocoStrategy(BaseInstallerStrategy):
    """Chocolatey Windows package manager strategy."""

    name: ClassVar[str] = "choco"

    def build_install_command(self, package_name: str, non_interactive: bool = True) -> list[str]:
        cmd = ["choco", "install", package_name]
        if non_interactive:
            cmd.append("-y")
        return cmd


class PackageInstaller:
    """Manages strategy selection and orchestrates tool installations."""

    AVAILABLE_STRATEGIES: tuple[type[BaseInstallerStrategy], ...] = (
        AptStrategy,
        PacmanStrategy,
        DnfStrategy,
        BrewStrategy,
        WingetStrategy,
        ChocoStrategy,
    )

    @classmethod
    def get_preferred_strategy(cls) -> BaseInstallerStrategy | None:
        """Detect and instantiate the most suitable package manager on the host."""
        for strat_cls in cls.AVAILABLE_STRATEGIES:
            if strat_cls.is_available():
                return strat_cls()
        return None

    @classmethod
    def install(
        cls,
        tool: ToolDefinition,
        strategy_name: str | None = None,
        dry_run: bool = False,
        non_interactive: bool = True,
        timeout: int = 300,
    ) -> InstallationResult:
        """
        Install the specified tool using a detected or designated package manager strategy.
        """
        current_os = PlatformManager.get_os_type()

        # 1. Platform check
        if not tool.is_platform_supported(current_os):
            msg = f"Cannot install '{tool.display_name}': unsupported on platform '{current_os}'."
            logger.error(msg)
            return InstallationResult(
                success=False,
                tool_name=tool.name,
                package_manager=None,
                message=msg,
                dry_run=dry_run,
            )

        # 2. Select strategy
        strategy: BaseInstallerStrategy | None = None
        if strategy_name:
            for s_cls in cls.AVAILABLE_STRATEGIES:
                if s_cls.name.lower() == strategy_name.lower() or (
                    strategy_name.lower() in ("apt", "apt-get") and s_cls == AptStrategy
                ):
                    if not s_cls.is_available():
                        msg = f"Requested package manager '{strategy_name}' is not installed or available on PATH."
                        logger.error(msg)
                        return InstallationResult(
                            success=False,
                            tool_name=tool.name,
                            package_manager=strategy_name,
                            message=msg,
                            dry_run=dry_run,
                        )
                    strategy = s_cls()
                    break
        else:
            strategy = cls.get_preferred_strategy()

        if not strategy:
            custom_hint = tool.custom_install_instructions.get(current_os, "")
            msg = (
                f"No supported package manager detected for platform '{current_os}'. "
                f"Cannot automatically install '{tool.display_name}'."
            )
            if custom_hint:
                msg += f" Suggested manual command: {custom_hint}"
            logger.error(msg)
            return InstallationResult(
                success=False,
                tool_name=tool.name,
                package_manager=None,
                message=msg,
                dry_run=dry_run,
            )

        # 3. Execute installation
        return strategy.execute_install(
            tool=tool,
            dry_run=dry_run,
            non_interactive=non_interactive,
            timeout=timeout,
        )
