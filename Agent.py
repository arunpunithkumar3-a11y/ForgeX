"""from forgeX.security.models import CommandRequest, ValidationResult
from utils import DENIED_EXECUTABLES


class SecurityManager:
    def __init__(self):
        pass

    def _executable(self, config: CommandRequest) -> bool:
        exe_command = config.executable
        if exe_command in DENIED_EXECUTABLES:
            return ValidationResult(
                allowed=False, reason=f"Executable {exe_command} is denied"
            )
        return ValidationResult(allowed=True)

"""

if __name__ == "__main__":
    """d = CommandRequest(executable="pip", args=[], cwd="")
    print(SecurityManager()._executable(d))"""
    from pathlib import Path

    print(
        Path("Agent.py")
        .resolve()
        .is_relative_to(r"C:\Users\DVS\OneDrive\Desktop\hackerrank")
    )
