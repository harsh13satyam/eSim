"""
Platform and OS detection abstraction for eSim Tool Manager.
"""

from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path


class PlatformManager:
    """Provides operating system and hardware architecture detection."""

    @staticmethod
    def get_os_type() -> str:
        """Return standardized OS family: 'linux', 'windows', 'darwin', or 'unknown'."""
        system = platform.system().lower()
        if "linux" in system:
            return "linux"
        if "windows" in system:
            return "windows"
        if "darwin" in system:
            return "darwin"
        return "unknown"

    @staticmethod
    def get_os_name_and_version() -> tuple[str, str]:
        """Detect human-readable OS name and version number."""
        os_type = PlatformManager.get_os_type()

        if os_type == "linux":
            # Python 3.10+ provides platform.freedesktop_os_release
            try:
                if hasattr(platform, "freedesktop_os_release"):
                    release_info = platform.freedesktop_os_release()
                    name = release_info.get("NAME") or release_info.get("PRETTY_NAME", "Linux")
                    version = release_info.get("VERSION_ID", release_info.get("VERSION", ""))
                    return name, version
            except Exception:
                pass

            # Fallback to /etc/os-release parsing
            os_release_path = Path("/etc/os-release")
            if os_release_path.exists():
                try:
                    data: dict[str, str] = {}
                    for line in os_release_path.read_text(encoding="utf-8").splitlines():
                        if "=" in line and not line.strip().startswith("#"):
                            k, v = line.strip().split("=", 1)
                            data[k] = v.strip('"\'')
                    name = data.get("NAME", data.get("PRETTY_NAME", "Linux"))
                    version = data.get("VERSION_ID", data.get("VERSION", ""))
                    return name, version
                except Exception:
                    pass
            return "Linux", platform.release()

        if os_type == "windows":
            win_ver = platform.win32_ver()
            return f"Windows {win_ver[0]}", win_ver[1]

        if os_type == "darwin":
            mac_ver = platform.mac_ver()
            return "macOS", mac_ver[0]

        return platform.system(), platform.release()

    @staticmethod
    def get_architecture() -> str:
        """Return host processor architecture (e.g., x86_64, aarch64, arm64)."""
        machine = platform.machine()
        return machine or "unknown"

    @staticmethod
    def is_admin() -> bool:
        """Check if current process has administrative/root privileges."""
        os_type = PlatformManager.get_os_type()
        if os_type in ("linux", "darwin"):
            if hasattr(os, "geteuid"):
                return os.geteuid() == 0
            return False
        if os_type == "windows":
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore[attr-defined]
            except Exception:
                return False
        return False

    @staticmethod
    def find_executable(name: str, custom_paths: list[Path] | None = None) -> Path | None:
        """
        Locate executable on system PATH or within custom directories.
        Handles platform-specific extensions like .exe on Windows.
        """
        # First check custom paths if provided
        if custom_paths:
            for base_dir in custom_paths:
                candidate = base_dir / name
                if candidate.is_file() and os.access(candidate, os.X_OK):
                    return candidate.resolve()
                if PlatformManager.get_os_type() == "windows":
                    exe_candidate = base_dir / f"{name}.exe"
                    if exe_candidate.is_file() and os.access(exe_candidate, os.X_OK):
                        return exe_candidate.resolve()

        # Fallback to standard system PATH search
        found = shutil.which(name)
        if found:
            return Path(found).resolve()

        # On Windows, try explicit .exe if not present in name
        if PlatformManager.get_os_type() == "windows" and not name.lower().endswith(".exe"):
            found = shutil.which(f"{name}.exe")
            if found:
                return Path(found).resolve()

        return None
