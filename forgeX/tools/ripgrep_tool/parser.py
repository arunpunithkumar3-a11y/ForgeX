from forgeX.tools.ripgrep_tool.models import SearchRequest


def build_rg_command(req: SearchRequest) -> list[str]:
    if not req.pattern.strip():
        raise ValueError("Search pattern cannot be empty.")

    # We validate existence and directory status of root outside in the tool,
    # but we can do a sanity check here.

    cmd = [
        "rg",
        "--json",
        "--line-number",
        "--column",
        "--color=never",
        "--with-filename",
        "--max-count",
        str(req.max_results),
    ]

    if req.literal:
        cmd.append("--fixed-strings")

    if not req.case_sensitive:
        cmd.append("--ignore-case")

    if req.whole_word:
        cmd.append("--word-regexp")

    if req.include_hidden:
        cmd.append("--hidden")

    if req.file_globs:
        for glob in req.file_globs:
            cmd.extend(["--glob", glob])

    if req.exclude_globs:
        for glob in req.exclude_globs:
            cmd.extend(["--glob", f"!{glob}"])

    cmd.extend(
        [
            req.pattern,
            str(req.root),
        ]
    )

    return cmd
