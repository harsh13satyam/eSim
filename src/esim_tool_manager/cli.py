"""
Command Line Interface for eSim Automated Tool Manager.
Provides commands: check, list, install, version, info, doctor.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from esim_tool_manager.exceptions import (
    InvalidToolNameError,
    ToolManagerError,
    ToolNotFoundError,
)
from esim_tool_manager.logger import get_logger
from esim_tool_manager.manager import ToolManager
from esim_tool_manager.models import StatusEnum, ToolStatus

logger = get_logger("esim_manager.cli")


class Colors:
    """ANSI color codes with automatic detection and disabling."""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    _enabled = True

    @classmethod
    def enable(cls, val: bool) -> None:
        cls._enabled = val

    @classmethod
    def green(cls, text: str) -> str:
        return f"{cls.GREEN}{text}{cls.RESET}" if cls._enabled else text

    @classmethod
    def yellow(cls, text: str) -> str:
        return f"{cls.YELLOW}{text}{cls.RESET}" if cls._enabled else text

    @classmethod
    def red(cls, text: str) -> str:
        return f"{cls.RED}{text}{cls.RESET}" if cls._enabled else text

    @classmethod
    def cyan(cls, text: str) -> str:
        return f"{cls.CYAN}{text}{cls.RESET}" if cls._enabled else text

    @classmethod
    def bold(cls, text: str) -> str:
        return f"{cls.BOLD}{text}{cls.RESET}" if cls._enabled else text

    @classmethod
    def dim(cls, text: str) -> str:
        return f"{cls.DIM}{text}{cls.RESET}" if cls._enabled else text


def format_status_badge(status: StatusEnum) -> str:
    """Format status with colored symbol and label."""
    if status == StatusEnum.INSTALLED:
        return Colors.green(f"✓ {status.value}")
    if status == StatusEnum.MISSING:
        return Colors.red(f"✗ {status.value}")
    if status == StatusEnum.INCOMPATIBLE:
        return Colors.yellow(f"! {status.value}")
    if status == StatusEnum.UNSUPPORTED:
        return Colors.dim(f"⊘ {status.value}")
    return Colors.yellow(f"? {status.value}")


def cmd_check(manager: ToolManager, args: argparse.Namespace) -> int:
    """Execute dependency check across all tools."""
    sys_info = manager.get_system_info()
    statuses = manager.check_all_dependencies()

    if args.json:
        data = {
            "system": sys_info.to_dict(),
            "tools": [s.to_dict() for s in statuses],
        }
        print(json.dumps(data, indent=2))
        return 0

    print()
    print(Colors.bold("eSim Automated Tool Manager — Dependency Checker"))
    print("=" * 55)
    print(f"System: {Colors.cyan(sys_info.os_name)} ({sys_info.os_type}) | Arch: {sys_info.architecture}")
    print(f"Python: {sys_info.python_version} | Privileges: {'Root/Admin' if sys_info.is_admin else 'Standard User'}")
    if sys_info.available_package_managers:
        print(f"Package Managers: {', '.join(sys_info.available_package_managers)}")
    print("-" * 55)
    print()

    # Table Header
    col_tool = 14
    col_req = 10
    col_ver = 12
    col_stat = 16
    col_path = 24

    header = (
        f"{'TOOL':<{col_tool}} "
        f"{'REQUIRED':<{col_req}} "
        f"{'INSTALLED':<{col_ver}} "
        f"{'STATUS':<{col_stat}} "
        f"{'EXECUTABLE PATH'}"
    )
    print(Colors.bold(header))
    print("-" * 75)

    for s in statuses:
        ver_str = s.installed_version or "--"
        path_str = str(s.executable_path) if s.executable_path else "--"
        badge = format_status_badge(s.status)

        # Truncate path if very long
        if len(path_str) > 35:
            path_str = "..." + path_str[-32:]

        line = (
            f"{s.display_name:<{col_tool}} "
            f"{s.required_version:<{col_req}} "
            f"{ver_str:<{col_ver}} "
            f"{badge:<{col_stat + 9}} "  # extra width for ANSI codes
            f"{path_str}"
        )
        print(line)

    installed_count = sum(1 for s in statuses if s.status == StatusEnum.INSTALLED)
    missing_count = sum(1 for s in statuses if s.status == StatusEnum.MISSING)
    incompatible_count = sum(1 for s in statuses if s.status == StatusEnum.INCOMPATIBLE)

    print("-" * 75)
    print(
        f"Summary: {len(statuses)} total | "
        f"{Colors.green(f'{installed_count} available')} | "
        f"{Colors.red(f'{missing_count} missing') if missing_count else '0 missing'} | "
        f"{Colors.yellow(f'{incompatible_count} incompatible') if incompatible_count else '0 incompatible'}"
    )
    print()
    return 0 if missing_count == 0 and incompatible_count == 0 else 1


def cmd_list(manager: ToolManager, args: argparse.Namespace) -> int:
    """List all supported tools in the registry."""
    tools = manager.list_supported_tools()

    if args.json:
        data = [
            {
                "name": t.name,
                "display_name": t.display_name,
                "category": t.category,
                "executable": t.executable,
                "minimum_version": t.minimum_version,
                "supported_platforms": t.supported_platforms,
                "description": t.description,
            }
            for t in tools
        ]
        print(json.dumps(data, indent=2))
        return 0

    print()
    print(Colors.bold("Supported eSim Tools & Integrations"))
    print("=" * 60)
    for t in tools:
        print(f"• {Colors.bold(t.display_name)} ({Colors.cyan(t.name)})")
        print(f"  Category   : {t.category}")
        print(f"  Executable : {t.executable}")
        print(f"  Min Version: {t.minimum_version}")
        print(f"  Platforms  : {', '.join(t.supported_platforms)}")
        print(f"  Description: {t.description}")
        print()
    return 0


def cmd_version(manager: ToolManager, args: argparse.Namespace) -> int:
    """Query version information for a specific tool."""
    try:
        status = manager.get_tool_version(args.tool)
    except ToolManagerError as err:
        print(Colors.red(f"Error: {err}"), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(status.to_dict(), indent=2))
        return 0

    print()
    print(f"Tool       : {Colors.bold(status.display_name)} ({status.name})")
    print(f"Status     : {format_status_badge(status.status)}")
    print(f"Installed  : {status.installed_version or '--'}")
    print(f"Required   : {status.required_version}")
    print(f"Executable : {status.executable_path or '--'}")
    print(f"Message    : {status.message}")
    print()
    return 0 if status.status == StatusEnum.INSTALLED else 1


def cmd_info(manager: ToolManager, args: argparse.Namespace) -> int:
    """Display comprehensive metadata for a specific tool."""
    try:
        tool = manager.get_tool_info(args.tool)
    except ToolManagerError as err:
        print(Colors.red(f"Error: {err}"), file=sys.stderr)
        return 1

    if args.json:
        data = {
            "name": tool.name,
            "display_name": tool.display_name,
            "category": tool.category,
            "executable": tool.executable,
            "alternate_executables": tool.alternate_executables,
            "minimum_version": tool.minimum_version,
            "package_names": tool.package_names,
            "supported_platforms": tool.supported_platforms,
            "description": tool.description,
            "docs_url": tool.docs_url,
            "custom_install_instructions": tool.custom_install_instructions,
        }
        print(json.dumps(data, indent=2))
        return 0

    print()
    print(Colors.bold(f"Tool Specification: {tool.display_name}"))
    print("=" * 50)
    print(f"Canonical Name       : {Colors.cyan(tool.name)}")
    print(f"Category             : {tool.category}")
    print(f"Primary Executable   : {tool.executable}")
    if tool.alternate_executables:
        print(f"Alternate Executables: {', '.join(tool.alternate_executables)}")
    print(f"Minimum Version      : {tool.minimum_version}")
    print(f"Supported Platforms  : {', '.join(tool.supported_platforms)}")
    if tool.package_names:
        print(f"Package Identifiers  : {tool.package_names}")
    if tool.docs_url:
        print(f"Documentation URL    : {tool.docs_url}")
    print(f"Description          : {tool.description}")
    print()
    return 0


def cmd_install(manager: ToolManager, args: argparse.Namespace) -> int:
    """Install an external tool via platform package manager."""
    try:
        tool_def = manager.get_tool_info(args.tool)
    except ToolManagerError as err:
        if args.json:
            print(json.dumps({"success": False, "error": str(err)}, indent=2))
        else:
            print(Colors.red(f"Error: {err}"), file=sys.stderr)
        return 1

    # Interactive confirmation if requested and not dry-run, json, or force
    if not args.yes and not args.dry_run and not args.json:
        print()
        print(Colors.bold(f"eSim Automated Installer: {tool_def.display_name}"))
        print("-" * 50)
        prompt_text = f"Proceed with installing '{tool_def.display_name}' on this system? [y/N]: "
        try:
            choice = input(prompt_text).strip().lower()
            if choice not in ("y", "yes"):
                print("Installation aborted by user.")
                return 0
        except (KeyboardInterrupt, EOFError):
            print("\nInstallation aborted.")
            return 0
    elif not args.json:
        print()
        print(Colors.bold(f"eSim Automated Installer: {tool_def.display_name}"))
        print("-" * 50)

    result = manager.install_tool(
        tool_name=args.tool,
        package_manager=args.pm,
        dry_run=args.dry_run,
        non_interactive=True,
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.success else 1

    if result.dry_run:
        print(Colors.cyan(result.message))
        if result.command_executed:
            print(f"Simulated Command: {' '.join(result.command_executed)}")
        print()
        return 0

    if result.success:
        print(Colors.green(f"✓ {result.message}"))
        print()
        return 0
    else:
        print(Colors.red(f"✗ {result.message}"))
        if result.stderr:
            print(Colors.dim(f"Details: {result.stderr.strip()}"))
        print()
        return 1


def cmd_doctor(manager: ToolManager, args: argparse.Namespace) -> int:
    """Run comprehensive system and dependency diagnostics."""
    diagnosis = manager.run_doctor()
    sys_info = diagnosis["system_info"]
    statuses: list[ToolStatus] = diagnosis["tool_statuses"]
    summary = diagnosis["summary"]
    recommendations: list[str] = diagnosis["recommendations"]

    if args.json:
        data = {
            "system": sys_info.to_dict(),
            "tools": [s.to_dict() for s in statuses],
            "summary": summary,
            "recommendations": recommendations,
        }
        print(json.dumps(data, indent=2))
        return 0 if summary["healthy"] else 1

    print()
    print(Colors.bold("eSim Automated Tool Manager — Doctor"))
    print("=" * 55)
    print("System Environment:")
    print(f"  OS           : {sys_info.os_name} ({sys_info.os_type})")
    print(f"  Architecture : {sys_info.architecture}")
    print(f"  Python       : {sys_info.python_version}")
    print(f"  Privileges   : {'Administrator / Root' if sys_info.is_admin else 'Standard User'}")
    pms = ", ".join(sys_info.available_package_managers) if sys_info.available_package_managers else "None detected"
    print(f"  Pkg Managers : {pms}")
    print()

    print("Tools Status:")
    for s in statuses:
        badge = format_status_badge(s.status)
        ver = s.installed_version or "Missing"
        print(f"  {s.display_name:<24} : {badge:<20} (Version: {ver})")
    print()

    print("Diagnostics & Recommendations:")
    if summary["healthy"]:
        print(Colors.green("  ✓ All essential eSim tools and dependencies are healthy and properly configured!"))
    else:
        for idx, rec in enumerate(recommendations, 1):
            print(f"  {idx}. {Colors.yellow(rec)}")
    print()
    return 0 if summary["healthy"] else 1


def build_parser() -> argparse.ArgumentParser:
    """Construct command line arguments parser."""
    # Common flags parent parser for subparsers
    shared_parser = argparse.ArgumentParser(add_help=False)
    shared_parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output results in JSON format for automated tooling and IDEs.",
    )
    shared_parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output.",
    )
    shared_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging.",
    )

    parser = argparse.ArgumentParser(
        prog="esim-manager",
        description="eSim Automated Tool Manager: Install, verify, and diagnose external EDA tools.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[shared_parser],
        epilog="""
Examples:
  esim-manager check
  esim-manager list
  esim-manager doctor
  esim-manager version ngspice
  esim-manager info kicad
  esim-manager install ngspice --dry-run
  esim-manager check --json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # Command: check
    subparsers.add_parser("check", parents=[shared_parser], help="Check dependencies and version compatibility.")

    # Command: list
    subparsers.add_parser("list", parents=[shared_parser], help="List all supported eSim tools.")

    # Command: version <tool>
    p_version = subparsers.add_parser("version", parents=[shared_parser], help="Display installed version of a tool.")
    p_version.add_argument("tool", help="Name of the tool (e.g. ngspice, kicad, git, python)")

    # Command: info <tool>
    p_info = subparsers.add_parser("info", parents=[shared_parser], help="Display detailed metadata for a tool.")
    p_info.add_argument("tool", help="Name of the tool (e.g. ngspice, kicad, git, python)")

    # Command: install <tool>
    p_install = subparsers.add_parser("install", parents=[shared_parser], help="Install a tool using the system package manager.")
    p_install.add_argument("tool", help="Name of the tool to install (e.g. ngspice, kicad)")
    p_install.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the installation without modifying the system.",
    )
    p_install.add_argument(
        "--pm",
        help="Explicitly specify package manager (e.g. apt, winget, brew, pacman, dnf).",
    )
    p_install.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Automatically answer yes to confirmation prompts.",
    )

    # Command: doctor
    subparsers.add_parser("doctor", parents=[shared_parser], help="Run comprehensive environment diagnostics.")

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    # Handle color output configuration
    if args.no_color or "NO_COLOR" in os.environ or not sys.stdout.isatty():
        Colors.enable(False)
    else:
        Colors.enable(True)

    if not args.command:
        parser.print_help()
        return 0

    manager = ToolManager()

    try:
        if args.command == "check":
            return cmd_check(manager, args)
        elif args.command == "list":
            return cmd_list(manager, args)
        elif args.command == "version":
            return cmd_version(manager, args)
        elif args.command == "info":
            return cmd_info(manager, args)
        elif args.command == "install":
            return cmd_install(manager, args)
        elif args.command == "doctor":
            return cmd_doctor(manager, args)
        else:
            parser.print_help()
            return 1
    except Exception as exc:
        logger.exception(f"Unhandled exception during command '{args.command}': {exc}")
        print(Colors.red(f"Error: {exc}"), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
