"""
Unit tests for high-level ToolManager facade.
"""

import sys
import unittest
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from esim_tool_manager.exceptions import InvalidToolNameError, ToolNotFoundError
from esim_tool_manager.manager import ToolManager
from esim_tool_manager.models import StatusEnum


class TestToolManager(unittest.TestCase):
    """Test suite for ToolManager facade."""

    def setUp(self) -> None:
        self.manager = ToolManager()

    def test_list_supported_tools(self) -> None:
        """Verify list of supported tools contains core dependencies."""
        tools = self.manager.list_supported_tools()
        names = [t.name for t in tools]
        self.assertIn("python", names)
        self.assertIn("git", names)
        self.assertIn("ngspice", names)
        self.assertIn("kicad", names)

    def test_check_all_dependencies(self) -> None:
        """Verify checking all dependencies returns results for all registered tools."""
        statuses = self.manager.check_all_dependencies()
        self.assertEqual(len(statuses), 4)
        names = [s.name for s in statuses]
        self.assertIn("python", names)
        self.assertIn("git", names)

    def test_check_single_tool(self) -> None:
        """Verify checking a single named tool."""
        status = self.manager.check_single_tool("python")
        self.assertEqual(status.name, "python")
        self.assertEqual(status.status, StatusEnum.INSTALLED)

    def test_get_tool_info(self) -> None:
        """Verify retrieving tool metadata."""
        tool = self.manager.get_tool_info("ngspice")
        self.assertEqual(tool.name, "ngspice")
        self.assertEqual(tool.executable, "ngspice")
        self.assertEqual(tool.minimum_version, "38.0.0")

    def test_invalid_tool_name_raises(self) -> None:
        """Verify proper exceptions are raised for invalid or missing tools."""
        with self.assertRaises(InvalidToolNameError):
            self.manager.get_tool_info("")

        with self.assertRaises(ToolNotFoundError):
            self.manager.get_tool_info("unknown_eda_simulator_99")

    def test_run_doctor(self) -> None:
        """Verify doctor returns comprehensive diagnostics report."""
        report = self.manager.run_doctor()
        self.assertIn("system_info", report)
        self.assertIn("tool_statuses", report)
        self.assertIn("summary", report)
        self.assertIn("recommendations", report)
        self.assertEqual(report["summary"]["total"], 4)


if __name__ == "__main__":
    unittest.main()
