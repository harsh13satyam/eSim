"""
Unit tests for CLI interface commands and formatting.
"""

import io
import json
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from esim_tool_manager.cli import main


class TestCLI(unittest.TestCase):
    """Test suite for CLI execution and output formats."""

    def run_cli(self, args: list[str]) -> tuple[int, str, str]:
        """Helper to invoke CLI main with arguments and capture stdout/stderr."""
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(args)
        return code, out.getvalue(), err.getvalue()

    def test_list_command(self) -> None:
        """Test 'esim-manager list' command."""
        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        self.assertIn("Supported eSim Tools", out)
        self.assertIn("Ngspice", out)
        self.assertIn("KiCad", out)

    def test_list_json_command(self) -> None:
        """Test 'esim-manager list --json'."""
        code, out, _ = self.run_cli(["list", "--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 4)
        names = [item["name"] for item in data]
        self.assertIn("python", names)
        self.assertIn("ngspice", names)

    def test_info_command_json(self) -> None:
        """Test 'esim-manager info ngspice --json'."""
        code, out, _ = self.run_cli(["info", "ngspice", "--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["name"], "ngspice")
        self.assertEqual(data["minimum_version"], "38.0.0")

    def test_version_command(self) -> None:
        """Test 'esim-manager version python'."""
        code, out, _ = self.run_cli(["version", "python"])
        self.assertEqual(code, 0)
        self.assertIn("Python Runtime", out)
        self.assertIn("INSTALLED", out)

    def test_install_dry_run(self) -> None:
        """Test 'esim-manager install ngspice --dry-run'."""
        code, out, _ = self.run_cli(["install", "ngspice", "--dry-run"])
        self.assertEqual(code, 0)
        self.assertIn("DRY RUN", out)

    def test_install_dry_run_json(self) -> None:
        """Test 'esim-manager install ngspice --dry-run --json'."""
        code, out, _ = self.run_cli(["install", "ngspice", "--dry-run", "--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertTrue(data["success"])
        self.assertTrue(data["dry_run"])
        self.assertEqual(data["tool_name"], "ngspice")

    def test_doctor_json(self) -> None:
        """Test 'esim-manager doctor --json'."""
        code, out, _ = self.run_cli(["doctor", "--json"])
        data = json.loads(out)
        self.assertIn("system", data)
        self.assertIn("tools", data)
        self.assertIn("recommendations", data)


if __name__ == "__main__":
    unittest.main()
