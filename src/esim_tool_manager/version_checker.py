"""
Robust version extraction, parsing, and semantic comparison engine.
"""

from __future__ import annotations

import re
from esim_tool_manager.models import VersionComparisonResult


class VersionChecker:
    """Handles semantic and loose version parsing and requirement validation."""

    # Standard regular expressions for extracting version sequences from tool banners
    DEFAULT_VERSION_REGEX = r"(\d+(?:\.\d+)+(?:[a-zA-Z0-9_\-\.]*))"
    FALLBACK_SINGLE_DIGIT_REGEX = r"(?:version|release|v)?\s*(\d+(?:\.\d+)*)"

    @classmethod
    def extract_version(cls, output: str, regex_pattern: str | None = None) -> str | None:
        """
        Extract clean version string from raw stdout/stderr output.
        Handles banners from python, git, ngspice, kicad, etc.
        """
        if not output:
            return None

        # Clean output
        text = output.strip()

        # Specific pattern if supplied
        if regex_pattern:
            match = re.search(regex_pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()

        # Try default semantic version regex
        match = re.search(cls.DEFAULT_VERSION_REGEX, text)
        if match:
            # Clean trailing punct
            clean = match.group(1).rstrip(".-")
            return clean

        # Try fallback single/multi digit
        match = re.search(cls.FALLBACK_SINGLE_DIGIT_REGEX, text, re.IGNORECASE)
        if match:
            return match.group(1).rstrip(".-")

        return None

    @classmethod
    def parse_version_tuple(cls, version_str: str) -> tuple[int, ...]:
        """
        Convert a version string into a comparable tuple of integers.
        E.g. '3.12.4' -> (3, 12, 4)
             '42.2'   -> (42, 2, 0)
             '7.0.1-0' -> (7, 0, 1)
        """
        if not version_str:
            return (0, 0, 0)

        # Extract numeric segments
        numeric_parts = re.findall(r"\d+", version_str)
        if not numeric_parts:
            return (0, 0, 0)

        ints = [int(p) for p in numeric_parts]

        # Pad to standard 3-part (major, minor, patch) if shorter
        while len(ints) < 3:
            ints.append(0)

        return tuple(ints)

    @classmethod
    def compare(cls, installed: str | None, required: str) -> VersionComparisonResult:
        """
        Compare installed version string with minimum required version string.
        Returns VersionComparisonResult.
        """
        if not installed:
            return VersionComparisonResult(
                installed_version="",
                required_version=required,
                satisfies=False,
                details="No installed version detected.",
            )

        installed_tuple = cls.parse_version_tuple(installed)
        required_tuple = cls.parse_version_tuple(required)

        satisfies = installed_tuple >= required_tuple

        if satisfies:
            details = f"Installed version {installed} satisfies minimum requirement {required}."
        else:
            details = f"Installed version {installed} is lower than required minimum {required}."

        return VersionComparisonResult(
            installed_version=installed,
            required_version=required,
            satisfies=satisfies,
            details=details,
        )
