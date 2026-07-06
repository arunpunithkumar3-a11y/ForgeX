import sys
import time
from pathlib import Path

# Add project root to sys.path so 'tools' can be imported when running script directly
project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.append(project_root)

import docker
from docker.models.containers import Container
from tools.sandbox.backend import SandboxBackend
from tools.sandbox.models import SandboxConfig, CommandResult, SandboxStatus


class DockerBackend(SandboxBackend):
    def __init__(self, config: SandboxConfig):
        self.config = config
        self._client: docker.DockerClient | None = None
        self.container: Container | None = None

    @property
    def client(self) -> docker.DockerClient | None:
        """
        Lazily initialize the Docker client connected to the local Docker daemon.
        """
        if self._client is None:
            try:
                self._client = docker.from_env()
            except Exception as e:
                sys.stderr.write(f"Failed to connect to Docker daemon: {e}\n")
                return None
        return self._client

    def _create_container(self) -> Container | None:
        """
        Create a Docker container based on the sandbox configuration.
        """
        client = self.client
        if not client:
            return None
        try:
            return client.containers.create(
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
        except Exception as e:
            sys.stderr.write(f"Failed to create container: {e}\n")
            return None

    def _require_running_container(self) -> Container | None:
        """
        Ensure the container is running and return it.
        """
        client = self.client
        if not client:
            return None

        if self.container is None and self.config.container_name:
            try:
                self.container = client.containers.get(self.config.container_name)
            except Exception:
                pass

        if self.container is None:
            return None

        try:
            self.container.reload()
        except Exception:
            self.container = None
            return None

        if self.container.status != "running":
            return None

        return self.container

    def start(self) -> None:
        """
        Create and start the sandbox container.
        """
        client = self.client
        if not client:
            return

        try:
            if self.container:
                try:
                    self.container.reload()
                except Exception:
                    self.container = None

            if not self.container and self.config.container_name:
                try:
                    self.container = client.containers.get(self.config.container_name)
                except Exception:
                    pass

            if not self.container:
                self.container = self._create_container()

            if self.container and self.container.status != "running":
                self.container.start()
                self.container.reload()
        except Exception as e:
            sys.stderr.write(f"Error starting sandbox: {e}\n")

    def stop(self) -> None:
        """
        Stop the sandbox container.
        """
        if self.container:
            try:
                self.container.stop()
            except Exception as e:
                sys.stderr.write(f"Error stopping sandbox: {e}\n")
            finally:
                self.container = None

    def remove(self) -> None:
        """
        Permanently remove the sandbox container.
        """
        if self.container:
            try:
                self.container.remove(force=True)
            except Exception as e:
                sys.stderr.write(f"Error removing sandbox: {e}\n")
            finally:
                self.container = None



    def execute(
        self,
        command: str,
        timeout: int | None = None,
        working_directory: str | None = None,
    ) -> CommandResult:
        """
        Execute a shell command inside the sandbox container.
        """
        start = time.perf_counter()
        container = self._require_running_container()
        if not container:
            return CommandResult(
                success=False,
                command=command,
                exit_code=-1,
                stdout="",
                stderr="Sandbox error: Sandbox container is not running or available.",
                duration_ms=0.0
            )

        exec_timeout = timeout if timeout is not None else self.config.timeout
        if exec_timeout:
            cmd_to_run = ["timeout", str(exec_timeout), "sh", "-c", command]
        else:
            cmd_to_run = ["sh", "-c", command]

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
            stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
            stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
            return CommandResult(
                success=result.exit_code == 0,
                command=command,
                exit_code=result.exit_code,
                stdout=stdout,
                stderr=stderr,
                duration_ms=duration,
            )
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            return CommandResult(
                success=False,
                command=command,
                exit_code=-1,
                stdout="",
                stderr=f"Docker execution error: {e}",
                duration_ms=duration,
            )


config = SandboxConfig(
    image="python:3.12-slim",
    container_name="sandbox_container",
    working_directory="/workspace",
    workspace=Path.cwd(),
    auto_remove=True,
)

if __name__ == "__main__":
    # Demonstrate usage with context manager
    print("Initializing Sandbox Backend...")
    try:
        with DockerBackend(config) as backend:
            print("Sandbox started.")

            print("\nExecuting command 1 (should fail gracefully if not started):")
            res1 = backend.execute("python --version", timeout=120)
            print("CommandResult 1:")
            print(f"  Success: {res1.success}")
            print(f"  Exit code: {res1.exit_code}")
            print(f"  Stdout: {res1.stdout.strip()}")
            print(f"  Stderr: {res1.stderr.strip()}")
            print(f"  Duration: {res1.duration_ms:.2f}ms")

            print("\nExecuting command 2 (should fail gracefully if not started):")
            res2 = backend.execute("sleep 10", timeout=2)
            print("CommandResult 2:")
            print(f"  Success: {res2.success}")
            print(f"  Exit code: {res2.exit_code}")
            print(f"  Stdout: {res2.stdout.strip()}")
            print(f"  Stderr: {res2.stderr.strip()}")
            print(f"  Duration: {res2.duration_ms:.2f}ms")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    print("Done.")



