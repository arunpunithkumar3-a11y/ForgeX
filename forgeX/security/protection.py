from pathlib import Path

from forgeX.security.models import CommandRequest, ValidationResult
from utils import DENIED_EXECUTABLES


class SecurityManager:
    def __init__(self):
        pass

    def validate_executable(self, config: CommandRequest) -> ValidationResult:
        exe_command = config.executable
        if exe_command in DENIED_EXECUTABLES:
            return ValidationResult(
                allowed=False, reason=f"Executable {exe_command} is denied"
            )
        return ValidationResult(allowed=True)

    def validate_working_directory(self, config: CommandRequest) -> ValidationResult:
        try:
            workspace = Path(config.working_directory).resolve()
            cwd = Path(config.cwd).resolve()
        except Exception as e:
            return ValidationResult(
                allowed=False, reason=f"Invalid working directory: {e}"
            )

        if not cwd.is_relative_to(workspace):
            return ValidationResult(
                allowed=False, reason="Working directory is outside the workspace."
            )

        return ValidationResult(allowed=True)
