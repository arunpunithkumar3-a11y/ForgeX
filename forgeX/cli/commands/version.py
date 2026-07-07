import platform
import sys

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
panel = Panel(renderable=Table)


def version():

    sys_table = Table(show_header=False, box=False)

    sys_table.add_row("[bold green]ForgeX version[/bold green]", "v0.1.0")
    sys_table.add_row("[bold green]Python version[/bold green]", sys.version.split()[0])
    sys_table.add_row(
        "[bold green]Platform[/bold green]", f"{platform.system()} {platform.release()}"
    )
    panel = Panel(
        sys_table,
        title="[bold #875fdf]⚙️ ForgeX System Information[/bold #875fdf]",
        border_style="#875fdf",
        box=box.ROUNDED,
        expand=False,
        padding=(1, 2),
    )

    console.print(panel)
