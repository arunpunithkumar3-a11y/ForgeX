import shutil
from pathlib import Path

from forgeX.tools.Terminal.security.models import CommandRequest, ValidationResult
from utils import DENIED_EXECUTABLES


class SecurityManager:
    def __init__(self):
        pass

    def _validate_executable(self, config: CommandRequest) -> ValidationResult:
        exe = config.executable
        workspace = Path(config.workspace).resolve()

        # Collect all name variations to check against denied list
        names_to_check = {exe.lower()}
        
        try:
            exe_path = Path(exe)
            names_to_check.add(exe_path.name.lower())
            names_to_check.add(exe_path.stem.lower())
        except Exception:
            pass

        # Resolve command via system PATH
        try:
            resolved = shutil.which(exe)
            if resolved:
                resolved_path = Path(resolved)
                names_to_check.add(resolved_path.name.lower())
                names_to_check.add(resolved_path.stem.lower())
        except Exception:
            pass

        # Check against DENIED_EXECUTABLES
        denied_set = {d.lower() for d in DENIED_EXECUTABLES}
        for name in names_to_check:
            if name in denied_set:
                return ValidationResult(
                    allowed=False, reason=f"Executable '{exe}' is denied."
                )

        # If executable contains path separators, it represents a specific local path.
        # Ensure it resides inside the workspace!
        is_path = '/' in exe or '\\' in exe or exe.startswith('.') or (len(exe) >= 2 and exe[1] == ':')
        if is_path:
            try:
                cwd = Path(config.cwd).resolve()
                if not Path(exe).is_absolute():
                    abs_exe_path = (cwd / exe).resolve()
                else:
                    abs_exe_path = Path(exe).resolve()
                
                try:
                    abs_exe_path.relative_to(workspace)
                except ValueError:
                    return ValidationResult(
                        allowed=False,
                        reason=f"Executable path '{exe}' is outside the workspace."
                    )
            except Exception as e:
                return ValidationResult(
                    allowed=False,
                    reason=f"Invalid executable path '{exe}': {e}"
                )

        return ValidationResult(allowed=True, reason="")

    def _validate_working_directory(self, config: CommandRequest) -> ValidationResult:
        try:
            workspace = Path(config.workspace).resolve()
            cwd = Path(config.cwd).resolve()
        except Exception as e:
            return ValidationResult(
                allowed=False, reason=f"Invalid working directory: {e}"
            )

        try:
            cwd.relative_to(workspace)
        except ValueError:
            return ValidationResult(
                allowed=False, reason="Working directory is outside the workspace."
            )

        return ValidationResult(allowed=True, reason="")

    def _validate_path(self, config: CommandRequest) -> ValidationResult:
        try:
            workspace = Path(config.workspace).resolve()
            cwd = Path(config.cwd).resolve()
            args = config.args
            for arg in args:
                val = arg.value
                is_path = arg.is_path

                # Detect potential path-like values even if is_path is not set to True
                if not is_path:
                    if len(val) >= 2 and val[0].isalpha() and val[1] == ':':
                        is_path = True
                    elif val.startswith('/') or val.startswith('\\'):
                        is_path = True
                    elif '..' in val and ('/' in val or '\\' in val):
                        is_path = True

                if not is_path:
                    continue

                try:
                    clean_val = val.strip('"\'')
                    arg_path = Path(clean_val)
                    if not arg_path.is_absolute():
                        arg_path = (cwd / arg_path).resolve()
                    else:
                        arg_path = arg_path.resolve()
                    
                    try:
                        arg_path.relative_to(workspace)
                    except ValueError:
                        return ValidationResult(
                            allowed=False,
                            reason=f"Path '{val}' is outside the workspace.",
                        )
                except Exception as e:
                    if '..' in val:
                        return ValidationResult(
                            allowed=False,
                            reason=f"Invalid path or traversal in argument '{val}': {e}",
                        )

            return ValidationResult(allowed=True, reason="")
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
        return ValidationResult(allowed=True, reason="")
