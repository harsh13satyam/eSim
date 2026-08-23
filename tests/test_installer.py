"""
Unit tests for package installer and platform strategies.
"""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from esim_tool_manager.installer import (
    AptStrategy,
    BrewStrategy,
    ChocoStrategy,
    DnfStrategy,
    PackageInstaller,
    PacmanStrategy,
    WingetStrategy,
)
from esim_tool_manager.models import ToolDefinition


class TestPackageInstaller(unittest.TestCase):
    """Test suite for PackageInstaller and concrete installer strategies."""

    def setUp(self) -> None:
        self.tool = ToolDefinition(
            name="ngspice",
            display_name="Ngspice Circuit Simulator",
            description="Testing",
            executable="ngspice",
            package_names={
                "apt": "ngspice",
                "pacman": "ngspice",
                "dnf": "ngspice",
                "brew": "libngspice",
                "winget": "Ngspice.Ngspice",
                "choco": "ngspice",
            },
        )

    def test_apt_command_generation(self) -> None:
        """Test AptStrategy command generation."""
        strat = AptStrategy()
        cmd = strat.build_install_command("ngspice", non_interactive=True)
        self.assertIn("install", cmd)
        self.assertIn("-y", cmd)
        self.assertIn("ngspice", cmd)

    def test_pacman_command_generation(self) -> None:
        """Test PacmanStrategy command generation."""
        strat = PacmanStrategy()
        cmd = strat.build_install_command("ngspice", non_interactive=True)
        self.assertEqual(cmd, ["pacman", "-S", "--noconfirm", "ngspice"])

    def test_dnf_command_generation(self) -> None:
        """Test DnfStrategy command generation."""
        strat = DnfStrategy()
        cmd = strat.build_install_command("ngspice", non_interactive=True)
        self.assertEqual(cmd, ["dnf", "install", "-y", "ngspice"])

    def test_brew_command_generation(self) -> None:
        """Test BrewStrategy command generation."""
        strat = BrewStrategy()
        cmd = strat.build_install_command("libngspice", non_interactive=True)
        self.assertEqual(cmd, ["brew", "install", "libngspice"])

    def test_winget_command_generation(self) -> None:
        """Test WingetStrategy command generation."""
        strat = WingetStrategy()
        cmd = strat.build_install_command("Ngspice.Ngspice", non_interactive=True)
        self.assertIn("winget", cmd)
        self.assertIn("--exact", cmd)
        self.assertIn("Ngspice.Ngspice", cmd)

    def test_choco_command_generation(self) -> None:
        """Test ChocoStrategy command generation."""
        strat = ChocoStrategy()
        cmd = strat.build_install_command("ngspice", non_interactive=True)
        self.assertEqual(cmd, ["choco", "install", "ngspice", "-y"])

    def test_dry_run_execution(self) -> None:
        """Verify dry run generates valid simulation result without executing subprocess."""
        strat = AptStrategy()
        res = strat.execute_install(self.tool, dry_run=True)
        self.assertTrue(res.success)
        self.assertTrue(res.dry_run)
        self.assertIn("[DRY RUN]", res.message)
        self.assertIn("ngspice", " ".join(res.command_executed))

    @patch("subprocess.run")
    @patch("esim_tool_manager.platform.PlatformManager.is_admin")
    def test_mock_successful_install(self, mock_admin: MagicMock, mock_run: MagicMock) -> None:
        """Verify successful installation flow when subprocess returns 0."""
        mock_admin.return_value = True
        proc_mock = MagicMock()
        proc_mock.returncode = 0
        proc_mock.stdout = "Unpacking ngspice... Setting up ngspice..."
        proc_mock.stderr = ""
        mock_run.return_value = proc_mock

        strat = AptStrategy()
        res = strat.execute_install(self.tool, dry_run=False)

        self.assertTrue(res.success)
        self.assertEqual(res.return_code, 0)
        self.assertIn("Successfully installed", res.message)

    @patch("subprocess.run")
    @patch("esim_tool_manager.platform.PlatformManager.is_admin")
    def test_mock_failed_install(self, mock_admin: MagicMock, mock_run: MagicMock) -> None:
        """Verify failed installation flow when subprocess returns non-zero."""
        mock_admin.return_value = True
        proc_mock = MagicMock()
        proc_mock.returncode = 100
        proc_mock.stdout = ""
        proc_mock.stderr = "E: Unable to locate package ngspice"
        mock_run.return_value = proc_mock

        strat = AptStrategy()
        res = strat.execute_install(self.tool, dry_run=False)

        self.assertFalse(res.success)
        self.assertEqual(res.return_code, 100)
        self.assertIn("failed", res.message)


if __name__ == "__main__":
    unittest.main()
