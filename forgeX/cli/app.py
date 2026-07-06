import typer

from forgeX.cli.commands.init import init

app = typer.Typer(
    help="ForgeX - AI Coding Agent"
)

app.command()(init)


if __name__ == "__main__":
    app()