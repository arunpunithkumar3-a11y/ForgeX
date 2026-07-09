from pathlib import Path

from forgeX.tools.Terminal.security.models import CommandRequest, ValidationResult
from utils import DENIED_EXECUTABLES


class SecurityManager:
    def __init__(self):
        pass

    def _validate_executable(self, config: CommandRequest) -> ValidationResult:
        exe_command = config.executable
        if exe_command in DENIED_EXECUTABLES:
            return ValidationResult(
                allowed=False, reason=f"Executable {exe_command} is denied"
            )
        return ValidationResult(allowed=True)

    def _validate_working_directory(self, config: CommandRequest) -> ValidationResult:
        try:
            workspace = Path(config.workspace).resolve()
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

    def _validate_path(self, config: CommandRequest) -> ValidationResult:
        try:
            workspace = Path(config.workspace).resolve()
            cwd = Path(config.cwd).resolve()
            args = config.args
            for arg in args:
                if not arg.is_path:
                    continue
                arg_path = Path(arg.value)
                if not arg_path.is_absolute():
                    arg_path = (cwd / arg_path).resolve()
                else:
                    arg_path = arg_path.resolve()
                try:
                    arg_path.relative_to(workspace)
                except ValueError:
                    return ValidationResult(
                        allowed=False,
                        reason=f"Path '{arg_path}' is outside the workspace.",
                    )

            return ValidationResult(allowed=True)
        except Exception as e:
            return ValidationResult(allowed=False, reason=str(e))

    def validate(self, config: CommandRequest) -> ValidationResult:
        validators = (
            self._validate_executable,
            self._validate_working_directory,
            self._validate_path,
        )
        for val in validators:
            result = val(config)
            if not result.allowed:
                return result
        return ValidationResult(allowed=True)
