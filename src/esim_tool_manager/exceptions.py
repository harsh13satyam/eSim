"""
Exception classes for eSim Tool Manager.
"""


class ToolManagerError(Exception):
    """Base exception for all eSim Tool Manager errors."""

    def __init__(self, message: str, details: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class ToolNotFoundError(ToolManagerError):
    """Raised when a requested tool is not found in the registry or system."""
    pass


class InvalidToolNameError(ToolManagerError):
    """Raised when an invalid tool name is provided."""
    pass


class IncompatibleVersionError(ToolManagerError):
    """Raised when an installed tool does not meet the minimum version requirement."""
    pass


class InstallationError(ToolManagerError):
    """Raised when a tool installation fails or encounters an error."""
    pass


class UnsupportedPlatformError(ToolManagerError):
    """Raised when an operation or tool is not supported on the host platform."""
    pass


class PackageNotFoundError(InstallationError):
    """Raised when a package manager cannot locate the tool's package."""
    pass


class InsufficientPrivilegesError(InstallationError):
    """Raised when installation requires administrator/root privileges."""
    pass
