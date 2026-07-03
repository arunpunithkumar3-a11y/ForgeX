from abc import ABC, abstractmethod
from tools.sandbox.models import CommandResult,SandboxStatus


class SandboxBackend(ABC):
    """
    Abstract interface for all sandbox implementations.

    Every sandbox backend (Docker, Kubernetes, SSH, etc.)
    must implement this interface.
    """

    @abstractmethod
    def start(self) -> None:
        """
        Start the sandbox environment.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the sandbox environment.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self) -> None:
        """
        Remove the sandbox permanently.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        command: str,
        timeout: int | None = None,
        working_directory: str | None = None,
    ) -> CommandResult:
        """
        Execute a shell command inside the sandbox.
        """
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> SandboxStatus:
        """
        Return the current sandbox status.
        """
        raise NotImplementedError