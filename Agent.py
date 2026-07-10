from pathlib import Path

from forgeX.tools.ripgrep_tool.models import SearchRequest
from forgeX.tools.ripgrep_tool.parser import build_rg_command

if __name__ == "__main__":
    req = SearchRequest(
        pattern="TODO",
        root=Path("."),
        file_globs=["*.py", "*.md"],
        exclude_globs=["tests/", "build/"],
    )
    print(build_rg_command(req))
