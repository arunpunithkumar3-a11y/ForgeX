import sys
import time
from pathlib import Path
# Add project root to sys.path so 'tools' can be imported when running script directly
project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.append(project_root)

import docker
from docker.models.containers import Container
from tools.sandbox.models import SandboxConfig
from tools.sandbox.backend import SandboxBackend
import os 

from docker import DockerClient
from docker.models.containers import Container

from tools.sandbox.models import CommandResult, SandboxStatus


class DockerBackend(SandboxBackend):

    def __init__(self, config: SandboxConfig):
        self.config = config
        self.client: DockerClient = self._create_client()
        self.container: Container | None = None
        if self.config.container_name:
            try:
                self.container = self.client.containers.get(self.config.container_name)
            except docker.errors.NotFound:
                pass

    def _create_client(self) -> DockerClient:
        """
        Create a Docker client connected to the local Docker daemon.
        """
        return docker.from_env()

    def _create_container(self) -> Container:
        """
        Create a Docker container based on the sandbox configuration.
        """
        return self.client.containers.create(
            image=self.config.image,
            name=self.config.container_name,
            command=["tail", "-f", "/dev/null"],
            working_dir=self.config.working_directory,
            volumes={
                str(self.config.workspace): {
                    "bind": self.config.working_directory,
                    "mode": "rw",
                }
            },
            tty=True,
            detach=True,
            auto_remove=self.config.auto_remove,
        )
    def _require_running_container(self) -> Container:
        if self.container is None:
            raise RuntimeError("Sandbox has not been started.")

        self.container.reload()

        if self.container.status != "running":
            raise RuntimeError("Sandbox container is not running.")

        return self.container
    def start(self) -> None:
        """
        Create and start the sandbox container.
        """

        if self.container:
            try:
                self.container.reload()
            except docker.errors.NotFound:
                self.container = None


        if self.container is None and self.config.container_name:
            try:
                self.container = self.client.containers.get(self.config.container_name)
            except docker.errors.NotFound:
                pass

        if self.container is None:
            self.container = self._create_container()

        if self.container.status != "running":
            self.container.start()
            try:
                self.container.reload()
            except docker.errors.NotFound:

                self.container = None

    def stop(self) -> None:
        """
        Stop the sandbox container.
        """
        if self.container:
            try:
                self.container.stop()
                try:
                    self.container.reload()
                except (docker.errors.NotFound, docker.errors.APIError):
                    self.container = None
            except (docker.errors.NotFound, docker.errors.APIError):
                self.container = None

    def remove(self) -> None:
        """
        Permanently remove the sandbox container.
        """
        if self.container is None:
            return

        try:
            self.container.remove(force=True)
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as e:

            if "removal" in str(e) and "in progress" in str(e):
                pass
            else:
                raise e
        finally:
            self.container = None
    def get_status(self) -> SandboxStatus:
        """
        Return the current sandbox status.
        """
        if self.container is None:
            if self.config.container_name:
                try:
                    self.container = self.client.containers.get(self.config.container_name)
                except docker.errors.NotFound:
                    return SandboxStatus.REMOVED
            else:
                return SandboxStatus.REMOVED

        try:
            self.container.reload()
            status_map = {
                "created": SandboxStatus.CREATED,
                "running": SandboxStatus.RUNNING,
                "paused": SandboxStatus.RUNNING,
                "restarting": SandboxStatus.RUNNING,
                "removing": SandboxStatus.REMOVED,
                "exited": SandboxStatus.STOPPED,
                "dead": SandboxStatus.ERROR,
            }
            return status_map.get(self.container.status, SandboxStatus.ERROR)
        except docker.errors.NotFound:
            self.container = None
            return SandboxStatus.REMOVED
        except Exception:
            return SandboxStatus.ERROR

    def execute(
        self,
        command: str,
        timeout: int | None = None,
        working_directory: str | None = None,
    ) -> CommandResult:
        """
        Execute a shell command inside the sandbox container.
        """
        container = self._require_running_container()
        start = time.perf_counter()
        
        exec_timeout = timeout if timeout is not None else self.config.timeout
        # Wrap command in GNU timeout to enforce timeout limit inside the container
        cmd_to_run = ["timeout", str(exec_timeout), "sh", "-c", command]
        
        try:
            result = container.exec_run(
                cmd=cmd_to_run,
                workdir=working_directory or self.config.working_directory,
                stdout=True,
                stderr=True,
                demux=True,
            )
            duration = (time.perf_counter() - start) * 1000
            stdout_bytes, stderr_bytes = result.output or (None, None)
            stdout = (stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else "")
            stderr = (stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else "")
        except docker.errors.APIError as e:
            raise RuntimeError(f"Error occurred while executing command: {e}")
        return CommandResult(
            success=result.exit_code == 0,
            command=command,
            exit_code=result.exit_code,
            stdout=stdout,
            stderr=stderr,
            duration_ms=duration
        )


config = SandboxConfig(
    image="python:3.12-slim",
    container_name="sandbox_container",
    working_directory="/workspace",
    workspace=Path.cwd(),
    auto_remove=True,
)

if __name__ == "__main__":
    backend = DockerBackend(config)
    try:
        print("Starting sandbox...")
        backend.start()
        print("Sandbox started.")

        print("\nExecuting command 1 (should succeed):")
        res1 = backend.execute("git status", timeout=120)
        print("CommandResult 1:")
        print(f"  Success: {res1.success}")
        print(f"  Exit code: {res1.exit_code}")
        print(f"  Stdout: {res1.stdout.strip()}")
        print(f"  Stderr: {res1.stderr.strip()}")
        print(f"  Duration: {res1.duration_ms:.2f}ms")

        print("\nExecuting command 2 (should timeout after 2 seconds):")
        res2 = backend.execute("sleep 10", timeout=2)
        print("CommandResult 2:")
        print(f"  Success: {res2.success}")
        print(f"  Exit code: {res2.exit_code}")
        print(f"  Stdout: {res2.stdout.strip()}")
        print(f"  Stderr: {res2.stderr.strip()}")
        print(f"  Duration: {res2.duration_ms:.2f}ms")
    finally:
        print("\nStopping and removing sandbox...")
        """ backend.stop()
        backend.remove()"""
        print("Done.")



