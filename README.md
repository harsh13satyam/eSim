# eSim Automated Tool Manager

**FOSSEE eSim Semester Long Internship – Autumn 2026 Screening Task**  
**Task 5: Tool Manager (CSE and Related Fields)**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-green.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Tests: 36 Passed](https://img.shields.io/badge/tests-36%20passed-brightgreen.svg)](docs/TESTING.md)

---

## 1. Overview & Problem Statement

[eSim](https://esim.fossee.in/) is an open-source Electronic Design Automation (EDA) suite developed by FOSSEE at IIT Bombay. It integrates various third-party scientific software tools—such as **Ngspice** (circuit simulation), **KiCad** (schematic capture and PCB layout), **Python** (runtime and orchestration), and **Git** (version control).

Configuring, managing, and maintaining these external dependencies across heterogeneous platforms (Ubuntu, Debian, Fedora, Arch, Windows, macOS) often results in friction for students and researchers.

The **eSim Automated Tool Manager** is a modular, cross-platform Python system designed to automate tool inspection, dependency verification, version checking, platform-native installation, and diagnostics.

---

## 2. Requirements Implemented

This project fully implements the two core official screening task requirements:

- **Requirement 1: Tool Installation Management**
  - Cross-platform package management strategy abstraction (`apt`, `pacman`, `dnf`, `brew`, `winget`, `choco`).
  - Automated installation command resolution.
  - Safe subprocess execution without `shell=True`.
  - Non-destructive `--dry-run` simulation mode.
  - Transparent status reporting: never fakes installation success.
- **Requirement 4: Dependency Checker**
  - Host OS, distribution, kernel, architecture, and privilege detection.
  - Multi-candidate executable location resolution.
  - Robust version extraction from diverse CLI banners and SemVer comparison.
  - Status classification: `INSTALLED`, `MISSING`, `INCOMPATIBLE`, `UNKNOWN`, `UNSUPPORTED`.
  - Comprehensive `doctor` command with actionable diagnostic recommendations.
  - Machine-readable JSON output (`--json`) for automation.
- **Persistent Action Logging** (`logs/esim_manager.log`).

---

## 3. Project Architecture & Structure

```
esim-tool-manager/
├── src/
│   └── esim_tool_manager/
│       ├── __init__.py           # Package exports and version metadata
│       ├── cli.py               # Argument parsing and terminal formatting
│       ├── manager.py           # Core ToolManager facade
│       ├── models.py            # Typed dataclasses (ToolDefinition, ToolStatus, SystemInfo)
│       ├── detector.py          # System and tool dependency detector
│       ├── version_checker.py   # SemVer parser and version comparator
│       ├── installer.py         # Strategy pattern for package managers
│       ├── platform.py          # OS, architecture, and privilege heuristics
│       ├── logger.py            # Rotating file and console logger
│       ├── exceptions.py        # Exception hierarchy
│       └── tools/               # Pluggable tool registry
│           ├── __init__.py      # Registry lookup and dynamic registration
│           ├── base.py          # BaseToolProvider interface
│           ├── python.py        # Python runtime specification
│           ├── git.py           # Git version control specification
│           ├── ngspice.py       # Ngspice simulator specification
│           └── kicad.py         # KiCad EDA specification
│
├── tests/
│   ├── __init__.py
│   ├── test_detector.py         # Detector and platform tests
│   ├── test_version_checker.py  # Version parsing and comparison tests
│   ├── test_installer.py        # Strategy command generation and mock execution
│   ├── test_manager.py          # High-level ToolManager facade tests
│   ├── test_cli.py              # CLI commands and JSON output tests
│   └── test_tools.py            # Tool registry and dynamic extension tests
│
├── docs/
│   ├── DESIGN.md                # Comprehensive architecture and design document
│   └── TESTING.md               # Detailed test matrix and execution guide
│
├── logs/
│   └── esim_manager.log         # Rotated action and diagnostic log
│
├── main.py                      # Direct CLI execution entry point
├── pyproject.toml               # Modern PEP 518/621 packaging
├── requirements.txt             # Development and testing dependencies
└── README.md                    # Project documentation
```

---

## 4. Supported Tools (Default Registry)

| Tool Name | Display Name | Category | Primary Executable | Minimum Version | Supported Platforms |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `python` | Python Runtime | Core Runtime | `python3` | `>= 3.10.0` | Linux, Windows, macOS |
| `git` | Git Version Control | Version Control | `git` | `>= 2.20.0` | Linux, Windows, macOS |
| `ngspice` | Ngspice Circuit Simulator | Circuit Simulation | `ngspice` | `>= 38.0.0` | Linux, Windows, macOS |
| `kicad` | KiCad EDA Suite | Schematic & PCB Design | `kicad` | `>= 7.0.0` | Linux, Windows, macOS |

---

## 5. Quickstart & Usage

### 5.1 Direct Invocation (No Installation Required)

Using standard Python 3.10+:

```bash
# Check all dependencies
python main.py check

# Run comprehensive environment diagnostic
python main.py doctor

# List all supported tools in registry
python main.py list

# Query version of a specific tool
python main.py version python

# View detailed tool metadata
python main.py info ngspice

# Dry-run installation simulation
python main.py install ngspice --dry-run
```

### 5.2 Package Installation (Optional)

```bash
pip install -e .
esim-manager check
```

---

## 6. Example Terminal Outputs

### 6.1 Dependency Checker (`python main.py check`)

```text
eSim Automated Tool Manager — Dependency Checker
=======================================================
System: Debian GNU/Linux (linux) | Arch: x86_64
Python: 3.10.12 | Privileges: Root/Admin
Package Managers: apt-get, apt
-------------------------------------------------------

TOOL           REQUIRED   INSTALLED    STATUS           EXECUTABLE PATH
---------------------------------------------------------------------------
Python Runtime 3.10.0     3.10.12      ✓ INSTALLED      /usr/bin/python3.10
Git Control    2.20.0     2.34.1       ✓ INSTALLED      /usr/bin/git
Ngspice        38.0.0     --           ✗ MISSING        --
KiCad EDA      7.0.0      --           ✗ MISSING        --
---------------------------------------------------------------------------
Summary: 4 total | 2 available | 2 missing | 0 incompatible
```

### 6.2 Doctor Diagnostics (`python main.py doctor`)

```text
eSim Automated Tool Manager — Doctor
=======================================================
System Environment:
  OS           : Debian GNU/Linux (linux)
  Architecture : x86_64
  Python       : 3.10.12
  Privileges   : Administrator / Root
  Pkg Managers : apt-get, apt

Tools Status:
  Python Runtime           : ✓ INSTALLED          (Version: 3.10.12)
  Git Version Control      : ✓ INSTALLED          (Version: 2.34.1)
  Ngspice Circuit Simulator: ✗ MISSING            (Version: Missing)
  KiCad EDA Suite          : ✗ MISSING            (Version: Missing)

Diagnostics & Recommendations:
  1. Install missing dependency 'Ngspice Circuit Simulator' via: esim-manager install ngspice
  2. Install missing dependency 'KiCad EDA Suite' via: esim-manager install kicad
```

### 6.3 Dry-Run Installation (`python main.py install ngspice --dry-run`)

```text
eSim Automated Installer: Ngspice Circuit Simulator
--------------------------------------------------
[DRY RUN] Would execute command: 'apt-get install -y ngspice'
Simulated Command: apt-get install -y ngspice
```

### 6.4 JSON Output Mode (`python main.py check --json`)

```json
{
  "system": {
    "os_type": "linux",
    "os_name": "Debian GNU/Linux",
    "os_version": "12",
    "architecture": "x86_64",
    "python_version": "3.10.12",
    "is_admin": true,
    "available_package_managers": [
      "apt-get",
      "apt"
    ]
  },
  "tools": [
    {
      "name": "python",
      "display_name": "Python Runtime",
      "status": "INSTALLED",
      "symbol": "✓",
      "installed_version": "3.10.12",
      "required_version": "3.10.0",
      "executable_path": "/usr/bin/python3.10"
    }
  ]
}
```

---

## 7. Automated Testing

The project includes **36 unit tests** covering 100% of the core detection, parsing, installation strategies, and CLI logic.

Execute the test suite using Python's built-in `unittest` runner:

```bash
python3 -m unittest discover tests -v
```

All tests mock subprocess calls to ensure hermetic execution without requiring software installations or administrative privileges.

---

## 8. Security Considerations

- **No Shell Execution**: `shell=True` is completely prohibited across the codebase. All process execution uses explicit argument arrays (`subprocess.run(cmd_array, shell=False)`).
- **Input Validation**: All tool names are validated against the tool registry prior to invocation.
- **Privilege Separation**: Checking dependencies and diagnosing systems runs entirely under standard user permissions. Elevated privileges are only queried for package installation.
- **Log Privacy**: The logging subsystem avoids recording sensitive user data or credentials.

---

## 9. Design Extensibility

To add a new tool (e.g. `Verilator` or `OpenFOAM`), define a new class inheriting from `BaseToolProvider`:

```python
from esim_tool_manager.models import ToolDefinition
from esim_tool_manager.tools.base import BaseToolProvider
from esim_tool_manager.tools import register_tool

class VerilatorTool(BaseToolProvider):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="verilator",
            display_name="Verilator HDL Simulator",
            description="High-performance Verilog/SystemVerilog simulator.",
            executable="verilator",
            minimum_version="5.0.0",
            version_command=["--version"],
            version_regex=r"Verilator\s+(\d+(?:\.\d+)+)",
            package_names={
                "apt": "verilator",
                "brew": "verilator",
                "winget": "Verilator.Verilator",
            },
        )

register_tool(VerilatorTool())
```

---

## 10. Limitations & Future Improvements

- **Binary Compilations from Source**: Currently relies on system package managers. Future iterations could add sandboxed source compilation (e.g., building custom Ngspice patches).
- **GUI Integration**: Can be embedded into eSim's wxPython/Qt graphical workbench via the `ToolManager` Python API.
- **Library Updates**: Future versions can inspect Python package versions in eSim's virtual environment (e.g., `matplotlib`, `numpy`, `scipy`).
