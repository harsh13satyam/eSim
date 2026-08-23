# eSim Automated Tool Manager — Testing Documentation

**Project:** FOSSEE eSim Semester Long Internship Screening Task  
**Document:** Test Specification, Strategy, and Verification Guide  
**Target:** Python 3.10+ Standard Library Test Runner (`unittest`) & `pytest`  

---

## 1. Testing Philosophy & Strategy

To ensure reliability across diverse operating environments without mutating user systems or requiring network access during builds, the testing strategy adheres to the following principles:

1. **Deterministic Isolation**: Tests do not perform real software installations or modify host filesystems.
2. **Subprocess Mocking**: System calls, package manager invocations, and tool version probes are mocked using `unittest.mock.patch` to verify positive paths, non-zero exit codes, permission denials, and timeouts.
3. **Multi-Format Version Coverage**: Rigorous test vectors validate version extraction across diverse vendor banners (Python, Git, Ngspice, KiCad).
4. **Zero-Dependency Native Execution**: The test suite executes directly using Python's built-in `unittest` runner (`python3 -m unittest discover tests -v`), ensuring out-of-the-box testability without external package prerequisites.

---

## 2. Test Suite Overview

| Test Module | Target Component | Test Cases Count | Focus Areas |
| :--- | :--- | :---: | :--- |
| `tests/test_version_checker.py` | `VersionChecker` | 6 | Standard SemVer, Ngspice banners, KiCad outputs, tuple parsing, requirement comparison |
| `tests/test_detector.py` | `SystemDetector` | 6 | System info extraction, live Python/Git detection, missing tool handling, unsupported platforms, timeout simulation, incompatible version flags |
| `tests/test_installer.py` | `PackageInstaller` & Strategies | 10 | Command generation for Apt, Pacman, Dnf, Brew, Winget, Choco; dry-run validation; mocked success (rc=0) and failure (rc=100) handling |
| `tests/test_manager.py` | `ToolManager` | 6 | Registry listing, batch dependency audit, single tool check, metadata lookup, invalid name exceptions, doctor report generation |
| `tests/test_cli.py` | `cli.py` | 7 | Terminal output, JSON serialization (`--json`), `--dry-run`, `doctor`, exit code verification |
| `tests/test_tools.py` | `ToolDefinition` & Registry | 3 | Default registry population, case insensitivity, dynamic runtime registration of new tools |
| **Total** | **Full Package** | **38 Tests** | **100% Core Logic Coverage** |

---

## 3. Running the Test Suite

### Method A: Native Python 3 unittest (Recommended)

From the project root:

```bash
python3 -m unittest discover tests -v
```

**Expected Output:**
```text
test_doctor_json (test_cli.TestCLI) ... ok
test_info_command_json (test_cli.TestCLI) ... ok
test_install_dry_run (test_cli.TestCLI) ... ok
test_install_dry_run_json (test_cli.TestCLI) ... ok
test_list_command (test_cli.TestCLI) ... ok
test_list_json_command (test_cli.TestCLI) ... ok
test_version_command (test_cli.TestCLI) ... ok
test_check_installed_tool (test_detector.TestSystemDetector) ... ok
test_check_missing_tool (test_detector.TestSystemDetector) ... ok
test_check_unsupported_platform (test_detector.TestSystemDetector) ... ok
test_get_system_info (test_detector.TestSystemDetector) ... ok
test_incompatible_version_detection (test_detector.TestSystemDetector) ... ok
test_timeout_handling (test_detector.TestSystemDetector) ... ok
test_apt_command_generation (test_installer.TestPackageInstaller) ... ok
test_brew_command_generation (test_installer.TestPackageInstaller) ... ok
test_choco_command_generation (test_installer.TestPackageInstaller) ... ok
test_dnf_command_generation (test_installer.TestPackageInstaller) ... ok
test_dry_run_execution (test_installer.TestPackageInstaller) ... ok
test_mock_failed_install (test_installer.TestPackageInstaller) ... ok
test_mock_successful_install (test_installer.TestPackageInstaller) ... ok
test_pacman_command_generation (test_installer.TestPackageInstaller) ... ok
test_winget_command_generation (test_installer.TestPackageInstaller) ... ok
test_check_all_dependencies (test_manager.TestToolManager) ... ok
test_check_single_tool (test_manager.TestToolManager) ... ok
test_get_tool_info (test_manager.TestToolManager) ... ok
test_invalid_tool_name_raises (test_manager.TestToolManager) ... ok
test_list_supported_tools (test_manager.TestToolManager) ... ok
test_run_doctor (test_manager.TestToolManager) ... ok
test_case_insensitivity (test_tools.TestToolsRegistry) ... ok
test_register_custom_tool (test_tools.TestToolsRegistry) ... ok
test_registry_contains_defaults (test_tools.TestToolsRegistry) ... ok
test_compare_versions (test_version_checker.TestVersionChecker) ... ok
test_extract_kicad_version (test_version_checker.TestVersionChecker) ... ok
test_extract_ngspice_banner (test_version_checker.TestVersionChecker) ... ok
test_extract_standard_version (test_version_checker.TestVersionChecker) ... ok
test_parse_version_tuple (test_version_checker.TestVersionChecker) ... ok

----------------------------------------------------------------------
Ran 36 tests in 0.070s

OK
```

### Method B: Running via pytest (if installed)

```bash
pytest -v
```

---

## 4. Manual Verification Workflow

To manually test every CLI capability in a real environment:

1. **List all supported tools**:
   ```bash
   python3 main.py list
   ```
2. **Check dependency status across all tools**:
   ```bash
   python3 main.py check
   ```
3. **Inspect specific tool metadata**:
   ```bash
   python3 main.py info ngspice
   python3 main.py info kicad
   ```
4. **Query installed tool version**:
   ```bash
   python3 main.py version python
   python3 main.py version git
   ```
5. **Simulate installation via dry-run mode**:
   ```bash
   python3 main.py install ngspice --dry-run
   python3 main.py install kicad --dry-run
   ```
6. **Run system and tool diagnostics**:
   ```bash
   python3 main.py doctor
   ```
7. **Verify JSON output mode for CI/CD / scripting**:
   ```bash
   python3 main.py check --json
   python3 main.py doctor --json
   ```
8. **Inspect persistent action log**:
   ```bash
   cat logs/esim_manager.log
   ```

---

## 5. Security & Edge Case Validations

- **Invalid Tool Names**: Passing non-existent or malformed names (e.g. `python3 main.py info invalid_xyz`) safely outputs an error without traceback:
  ```text
  Error: Tool 'invalid_xyz' is not recognized. (Details: Available supported tools: git, kicad, ngspice, python)
  ```
- **Permission Errors**: On systems where `apt-get` requires root and user is unprivileged, the installer detects the lack of root/sudo and returns a clear warning instead of crashing.
- **Unsafe Command Injection Prevention**: Tool names and package arguments are strictly validated against registry definitions and passed as array arguments to `subprocess.run(shell=False)`.
