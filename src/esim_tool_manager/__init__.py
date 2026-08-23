"""
eSim Automated Tool Manager
===========================
A modular, cross-platform tool management, dependency verification,
and diagnostic engine for the eSim EDA suite.
"""

from esim_tool_manager.manager import ToolManager
from esim_tool_manager.models import ToolStatus, StatusEnum, InstallationResult, SystemInfo
from esim_tool_manager.exceptions import (
    ToolManagerError,
    ToolNotFoundError,
    IncompatibleVersionError,
    InstallationError,
    UnsupportedPlatformError,
)

__version__ = "1.0.0"
__all__ = [
    "ToolManager",
    "ToolStatus",
    "StatusEnum",
    "InstallationResult",
    "SystemInfo",
    "ToolManagerError",
    "ToolNotFoundError",
    "IncompatibleVersionError",
    "InstallationError",
    "UnsupportedPlatformError",
]
