import typer

from forgeX.cli.commands.config import config_app
from forgeX.cli.commands.doctor import doctor
from forgeX.cli.commands.init import init
from forgeX.cli.commands.models import models
from forgeX.cli.commands.providers import providers
from forgeX.cli.commands.version import version

app = typer.Typer(help="ForgeX - AI Coding Agent")

app.command()(init)
app.command()(version)
app.command()(providers)
app.command()(models)
app.command()(doctor)
app.add_typer(config_app, name="config")



@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        from forgeX.cli.ui.console import console
        from forgeX.cli.ui.panels import show_banner

        show_banner()
        console.print(" [bold #875fdf]Welcome to ForgeX![/bold #875fdf]")
        console.print(" To configure the AI coding agent environment, run:")
        console.print("   [bold #00d7ff]forgex init[/bold #00d7ff]\n")
        console.print(" For a list of all commands and options, run:")
        console.print("   [bold #00d7ff]forgex --help[/bold #00d7ff]\n")


if __name__ == "__main__":
    app()
