"""
Base interface and helper classes for tool definitions in eSim.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from esim_tool_manager.models import ToolDefinition


class BaseToolProvider(ABC):
    """Abstract provider interface for external tool definitions."""

    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """Return the immutable ToolDefinition for this tool."""
        raise NotImplementedError
