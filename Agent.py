from rich import box
from rich.panel import Panel
from rich.table import Table

from forgeX.cli.ui.console import console

table = Table(show_header=False, box=False)
table.add_column("[bold green]Provider[/bold green]")

table.add_row("[bold green]ForgeX version[/bold green]", "v0.1.0")
panel = Panel(
    table,
    title="[bold #875fdf]⚙️ ForgeX System Information[/bold #875fdf]",
    border_style="#875fdf",
    box=box.ROUNDED,
    expand=False,
    padding=(1, 2),
)

console.print(panel)
