"""
Unit tests for version parsing and comparison engine.
"""

import sys
import unittest
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from esim_tool_manager.models import VersionComparisonResult
from esim_tool_manager.tools.ngspice import extract_ngspice_version
from esim_tool_manager.tools.kicad import extract_kicad_version
from esim_tool_manager.version_checker import VersionChecker


class TestVersionChecker(unittest.TestCase):
    """Test suite for VersionChecker utility methods."""

    def test_extract_standard_version(self) -> None:
        """Test extraction from standard CLI version outputs."""
        self.assertEqual(
            VersionChecker.extract_version("Python 3.12.4"),
            "3.12.4",
        )
        self.assertEqual(
            VersionChecker.extract_version("git version 2.51.0"),
            "2.51.0",
        )
        self.assertEqual(
            VersionChecker.extract_version("git version 2.43.0 (Apple Git-143)"),
            "2.43.0",
        )

    def test_extract_ngspice_banner(self) -> None:
        """Test extraction from Ngspice complex banner strings."""
        banner1 = "** ngspice-42.2 : Circuit level simulation program\n** The U. C. Berkeley CAD Group"
        self.assertEqual(extract_ngspice_version(banner1, ""), "42.2")

        banner2 = "ngspice-38\nRelease date: 2022"
        self.assertEqual(extract_ngspice_version(banner2, ""), "38")

    def test_extract_kicad_version(self) -> None:
        """Test extraction from KiCad output formats."""
        kicad_out = "Application: kicad Version: 7.0.10, release build"
        self.assertEqual(extract_kicad_version(kicad_out, ""), "7.0.10")

        kicad_cli_out = "kicad-cli (8.0.0-rc1)"
        self.assertEqual(extract_kicad_version(kicad_cli_out, ""), "8.0.0")

    def test_parse_version_tuple(self) -> None:
        """Test conversion of version string into numeric tuple."""
        self.assertEqual(VersionChecker.parse_version_tuple("3.12.4"), (3, 12, 4))
        self.assertEqual(VersionChecker.parse_version_tuple("42.2"), (42, 2, 0))
        self.assertEqual(VersionChecker.parse_version_tuple("7"), (7, 0, 0))
        self.assertEqual(VersionChecker.parse_version_tuple("7.0.1-0"), (7, 0, 1, 0))
        self.assertEqual(VersionChecker.parse_version_tuple(""), (0, 0, 0))
        self.assertEqual(VersionChecker.parse_version_tuple("invalid"), (0, 0, 0))

    def test_compare_versions(self) -> None:
        """Test version comparison against requirements."""
        # Satisfied
        res1 = VersionChecker.compare("3.12.4", "3.10.0")
        self.assertTrue(res1.satisfies)

        res2 = VersionChecker.compare("42.2", "40.0.0")
        self.assertTrue(res2.satisfies)

        res3 = VersionChecker.compare("7.0.0", "7.0.0")
        self.assertTrue(res3.satisfies)

        # Incompatible (lower)
        res4 = VersionChecker.compare("3.8.10", "3.10.0")
        self.assertFalse(res4.satisfies)

        res5 = VersionChecker.compare("6.0.10", "7.0.0")
        self.assertFalse(res5.satisfies)

        # Missing / None
        res6 = VersionChecker.compare(None, "7.0.0")
        self.assertFalse(res6.satisfies)


if __name__ == "__main__":
    unittest.main()
