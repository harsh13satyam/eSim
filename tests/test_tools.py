"""
Unit tests for tool definitions and registry extensibility.
"""

import sys
import unittest
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools import (
    get_all_tools,
    get_tool,
    is_tool_registered,
    register_tool,
)


class TestToolsRegistry(unittest.TestCase):
    """Test suite for tool registry and dynamic extension."""

    def test_registry_contains_defaults(self) -> None:
        """Verify default tools are properly registered."""
        self.assertTrue(is_tool_registered("python"))
        self.assertTrue(is_tool_registered("git"))
        self.assertTrue(is_tool_registered("ngspice"))
        self.assertTrue(is_tool_registered("kicad"))

    def test_case_insensitivity(self) -> None:
        """Verify tool retrieval is case-insensitive."""
        t1 = get_tool("Ngspice")
        t2 = get_tool("NGSPICE")
        self.assertEqual(t1.name, t2.name)

    def test_register_custom_tool(self) -> None:
        """Verify registering a new tool dynamically."""
        custom = ToolDefinition(
            name="ghdl",
            display_name="GHDL VHDL Simulator",
            description="Open-source analyzer, compiler, and simulator for VHDL.",
            executable="ghdl",
            minimum_version="3.0.0",
            supported_platforms=["linux", "windows", "darwin"],
            category="HDL Simulation",
        )
        register_tool(custom)

        self.assertTrue(is_tool_registered("ghdl"))
        retrieved = get_tool("ghdl")
        self.assertEqual(retrieved.display_name, "GHDL VHDL Simulator")
        self.assertEqual(retrieved.category, "HDL Simulation")


if __name__ == "__main__":
    unittest.main()
