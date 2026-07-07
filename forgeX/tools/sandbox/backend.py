from abc import ABC, abstractmethod

from forgeX.tools.sandbox.models import CommandResult


class SandboxBackend(ABC):
    """
    Abstract interface for all sandbox implementations.
    """

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @abstractmethod
    def start(self) -> None:
        """Start the sandbox environment."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop the sandbox environment."""
        ...

    @abstractmethod
    def remove(self) -> None:
        """Remove the sandbox permanently."""
        ...

    @abstractmethod
    def execute(
        self,
        command: str,
        timeout: int | None = None,
        working_directory: str | None = None,
    ) -> CommandResult:
        """Execute a shell command inside the sandbox."""
        ...
