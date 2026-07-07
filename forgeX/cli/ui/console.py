import sys

from rich.console import Console

from forgeX.cli.ui.styles import FORGEX_THEME

# Reconfigure stdout/stderr to UTF-8 on Windows to safely print emojis and block characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(theme=FORGEX_THEME)
