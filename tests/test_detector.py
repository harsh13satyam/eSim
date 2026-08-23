"""
Unit tests for system and tool detection engine.
"""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from esim_tool_manager.detector import SystemDetector
from esim_tool_manager.models import StatusEnum, ToolDefinition
from esim_tool_manager.tools.python import PythonTool
from esim_tool_manager.tools.git import GitTool


class TestSystemDetector(unittest.TestCase):
    """Test suite for SystemDetector."""

    def test_get_system_info(self) -> None:
        """Verify system info returns valid metadata."""
        info = SystemDetector.get_system_info()
        self.assertIn(info.os_type, ("linux", "windows", "darwin", "unknown"))
        self.assertTrue(len(info.os_name) > 0)
        self.assertTrue(len(info.architecture) > 0)
        self.assertTrue(len(info.python_version) > 0)

    def test_check_installed_tool(self) -> None:
        """Verify detection of Python runtime (which must be running this test)."""
        py_tool = PythonTool().get_definition()
        status = SystemDetector.check_tool(py_tool)

        self.assertEqual(status.status, StatusEnum.INSTALLED)
        self.assertIsNotNone(status.installed_version)
        self.assertIsNotNone(status.executable_path)

    def test_check_missing_tool(self) -> None:
        """Verify handling of nonexistent tool binary."""
        dummy_tool = ToolDefinition(
            name="dummy-nonexistent-tool",
            display_name="Nonexistent Tool",
            description="Testing missing binary",
            executable="nonexistent_binary_xyz_12345",
            minimum_version="1.0.0",
        )
        status = SystemDetector.check_tool(dummy_tool)
        self.assertEqual(status.status, StatusEnum.MISSING)
        self.assertIsNone(status.executable_path)

    def test_check_unsupported_platform(self) -> None:
        """Verify status when tool does not support host platform."""
        tool = ToolDefinition(
            name="solaris-only-tool",
            display_name="Solaris Tool",
            description="Only runs on solaris",
            executable="solaris_tool",
            supported_platforms=["solaris"],
        )
        status = SystemDetector.check_tool(tool)
        self.assertEqual(status.status, StatusEnum.UNSUPPORTED)

    @patch("subprocess.run")
    @patch("esim_tool_manager.platform.PlatformManager.find_executable")
    def test_timeout_handling(self, mock_find: MagicMock, mock_run: MagicMock) -> None:
        """Verify graceful error reporting when version probe times out."""
        mock_find.return_value = Path("/usr/bin/mock_tool")
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["mock_tool", "--version"], timeout=10)

        tool = ToolDefinition(
            name="mock_tool",
            display_name="Mock Tool",
            description="Mock timeout",
            executable="mock_tool",
        )
        status = SystemDetector.check_tool(tool)
        self.assertEqual(status.status, StatusEnum.UNKNOWN)
        self.assertIn("Timed out", status.message)

    @patch("subprocess.run")
    @patch("esim_tool_manager.platform.PlatformManager.find_executable")
    def test_incompatible_version_detection(self, mock_find: MagicMock, mock_run: MagicMock) -> None:
        """Verify INCOMPATIBLE status when tool version is below requirement."""
        mock_find.return_value = Path("/usr/bin/ngspice")
        proc_mock = MagicMock()
        proc_mock.stdout = "** ngspice-34 : Circuit level simulation program"
        proc_mock.stderr = ""
        proc_mock.returncode = 0
        mock_run.return_value = proc_mock

        tool = ToolDefinition(
            name="ngspice",
            display_name="Ngspice",
            description="Ngspice test",
            executable="ngspice",
            minimum_version="38.0.0",
        )
        status = SystemDetector.check_tool(tool)
        self.assertEqual(status.status, StatusEnum.INCOMPATIBLE)
        self.assertEqual(status.installed_version, "34")


if __name__ == "__main__":
    unittest.main()
