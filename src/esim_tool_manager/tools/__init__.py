"""
Tool registry and discovery subsystem for eSim Tool Manager.
"""

from __future__ import annotations

from typing import Dict
from esim_tool_manager.exceptions import InvalidToolNameError, ToolNotFoundError
from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools.base import BaseToolProvider
from esim_tool_manager.tools.python import PythonTool
from esim_tool_manager.tools.git import GitTool
from esim_tool_manager.tools.ngspice import NgspiceTool
from esim_tool_manager.tools.kicad import KiCadTool

_TOOL_REGISTRY: Dict[str, ToolDefinition] = {}


def register_tool(provider_or_def: BaseToolProvider | ToolDefinition) -> None:
    """Register a tool definition into the global manager registry."""
    if isinstance(provider_or_def, BaseToolProvider):
        definition = provider_or_def.get_definition()
    elif isinstance(provider_or_def, ToolDefinition):
        definition = provider_or_def
    else:
        raise ValueError(f"Expected BaseToolProvider or ToolDefinition, got {type(provider_or_def)}")

    _TOOL_REGISTRY[definition.name.lower()] = definition


def get_all_tools() -> list[ToolDefinition]:
    """Return a list of all registered tool definitions."""
    if not _TOOL_REGISTRY:
        _initialize_default_registry()
    return list(_TOOL_REGISTRY.values())


def get_tool(name: str) -> ToolDefinition:
    """
    Retrieve tool definition by name.
    Raises InvalidToolNameError if name is empty or invalid format.
    Raises ToolNotFoundError if tool is not registered.
    """
    if not name or not isinstance(name, str) or not name.strip():
        raise InvalidToolNameError("Tool name cannot be empty or non-string.")

    clean_name = name.strip().lower()

    if not _TOOL_REGISTRY:
        _initialize_default_registry()

    if clean_name in _TOOL_REGISTRY:
        return _TOOL_REGISTRY[clean_name]

    # Check aliases / executables
    for tool_def in _TOOL_REGISTRY.values():
        if clean_name == tool_def.executable.lower() or clean_name in [
            alt.lower() for alt in tool_def.alternate_executables
        ]:
            return tool_def

    available = ", ".join(sorted(_TOOL_REGISTRY.keys()))
    raise ToolNotFoundError(
        f"Tool '{name}' is not recognized.",
        details=f"Available supported tools: {available}",
    )


def is_tool_registered(name: str) -> bool:
    """Check if a tool exists in the registry."""
    try:
        get_tool(name)
        return True
    except (InvalidToolNameError, ToolNotFoundError):
        return False


def _initialize_default_registry() -> None:
    """Initialize registry with the core eSim EDA dependencies."""
    _TOOL_REGISTRY.clear()
    register_tool(PythonTool())
    register_tool(GitTool())
    register_tool(NgspiceTool())
    register_tool(KiCadTool())


# Initialize on import
_initialize_default_registry()
