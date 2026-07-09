import subprocess

from forgeX.tools.Terminal.security.models import CommandArgument, CommandRequest

if __name__ == "__main__":
    result = subprocess.run(
        ["pip", "install", "langchain"],
        capture_output=True,
        check=True,
        text=True,
        shell=False,
    )
    print(result)
    d = CommandRequest(
        executable="pip",
        args=[
            CommandArgument(value="install", is_path=False),
            CommandArgument(value="google", is_path=False),
        ],
        cwd="",
        workspace="",
        timeout=2,
    )
    command = [d.executable] + [x.value for x in d.args]
