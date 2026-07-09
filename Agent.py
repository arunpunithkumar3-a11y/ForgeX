from pathlib import Path
from forgeX.tools.Terminal.terminal_tool import TerminalTool

if __name__ == "__main__":
    # Create the tool, default workspace will be the current directory
    tool = TerminalTool()
    result = tool.invoke(
        {
            "executable": "python",
            "args": [{"value": "s.py", "is_path": True}],
            "cwd": "",
            "timeout": 120,
        }
    )
    print(result)
