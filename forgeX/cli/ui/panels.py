from rich import box
from rich.panel import Panel

from forgeX.cli.ui.console import console

BANNER_LINES = [
    (r" ███████╗ ██████╗ ██████╗  ██████╗ ███████╗██╗  ██╗", "#875fdf"),
    (r" ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚██╗██╔╝", "#7a76e7"),
    (r" █████╗  ██║   ██║██████╔╝██║  ███╗█████╗   ╚███╔╝ ", "#698eed"),
    (r" ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝   ██╔██╗ ", "#55a5f3"),
    (r" ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗██╔╝ ██╗", "#39bcf8"),
    (r" ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝", "#00d7ff"),
]


def show_banner() -> None:
    console.print()
    for line, color in BANNER_LINES:
        console.print(line, style=f"bold {color}")

    console.print(
        " [bold #875fdf]⚒ ForgeX[/bold #875fdf] | [bold #00d7ff]Next-Gen AI Coding Agent[/bold #00d7ff] [dim white]v0.1.0[/dim white]"
    )
    console.print(" " + "[#8a8a8a]━" * 54 + "[/#8a8a8a]")
    console.print()


def success(message: str) -> None:
    console.print(
        Panel(
            f" [bold #00ff87]✔ Success:[/bold #00ff87] {message}",
            border_style="#00ff87",
            box=box.ROUNDED,
            expand=False,
        )
    )


def error(message: str) -> None:
    console.print(
        Panel(
            f" [bold #ff5f87]✘ Error:[/bold #ff5f87] {message}",
            border_style="#ff5f87",
            box=box.ROUNDED,
            expand=False,
        )
    )


def warning(message: str) -> None:
    console.print(
        Panel(
            f" [bold #ffaf5f]⚠ Warning:[/bold #ffaf5f] {message}",
            border_style="#ffaf5f",
            box=box.ROUNDED,
            expand=False,
        )
    )


def info(message: str) -> None:
    console.print(
        Panel(
            f" [bold #5f87ff]ℹ Info:[/bold #5f87ff] {message}",
            border_style="#5f87ff",
            box=box.ROUNDED,
            expand=False,
        )
    )
