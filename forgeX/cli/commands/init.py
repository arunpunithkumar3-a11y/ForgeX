import questionary
from rich.console import Console
from forgeX.config.env_manager import EnvironmentManager
from forgeX.config.manager import ConfigManager
from forgeX.config.constants import PROVIDERS

import questionary
from rich.console import Console

from forgeX.config.constants import PROVIDERS

console = Console()


def show_banner() -> None:
    banner = r"""
███████╗ ██████╗ ██████╗  ██████╗ ███████╗██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚██╗██╔╝
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗   ╚███╔╝
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝   ██╔██╗
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗██╔╝ ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

    console.print(banner, style="bold cyan")
    console.print("[bold green]⚒ ForgeX Setup[/bold green]\n")


def ask_provider() -> str:
    provider = questionary.select(
        "Select your LLM provider:",
        choices=list(PROVIDERS.keys()),
    ).ask()

    if provider is None:
        raise KeyboardInterrupt()

    return provider


def ask_model(provider: str) -> str:
    model = questionary.text(
        f"Enter the model name for {provider}:"
    ).ask()

    if model is None:
        raise KeyboardInterrupt()

    return model.strip()


def ask_api_key(provider: str) -> str | None:
    provider_metadata = PROVIDERS[provider]

    if not provider_metadata.requires_api_key:
        return None

    api_key = questionary.password(
        f"Enter your {provider} API key:"
    ).ask()

    if api_key is None:
        raise KeyboardInterrupt()

    return api_key.strip()



def init() -> None:
    try:
        show_banner()

        provider = ask_provider()
        model = ask_model(provider)
        api_key = ask_api_key(provider)

        console.print()
        console.print("[bold green]✓ Information collected successfully![/bold green]")
        console.print(f"Provider : {provider}")
        console.print(f"Model    : {model}")

        if api_key:
            console.print("API Key  : ********")

    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled by user.[/yellow]")