import platform
import sys

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# create a Console instance
console = Console()

# create a table
sys_table = Table(show_header=False, box=False)
sys_table.add_row("[bold green]ForgeX version[/bold green]", "v0.1.0")
sys_table.add_row("[bold green]Python version[/bold green]", sys.version.split()[0])
sys_table.add_row("[bold #875fdf]Platform[/bold #875fdf]", platform.platform())


panel = Panel(
    sys_table,
    title="[bold #875fdf]⚙️ FORGEX SYSTEM INFORMATION[/bold #875fdf]",
    border_style="#875fdf",
    box=box.ROUNDED,
    expand=False,
    padding=(1, 2),
)

console.print(panel)
