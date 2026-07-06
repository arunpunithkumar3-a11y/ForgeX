import os
from pathlib import Path
from dotenv import dotenv_values
from forgeX.config.constants import (
    CONFIG_DIR,
    ENV_FILE,
    DEFAULT_ENV,
    PROVIDERS,
)
from forgeX.config.models import ProviderMetadata

class EnvironmentManager:
    """
    Manages loading, saving, and querying API keys from the ForgeX .env file,
    falling back to system environment variables. Resolves provider details
    dynamically using the global PROVIDERS registry.
    """

    def __init__(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not self.exists():
            self.create()

    def create(self) -> None:
        """Creates the .env file with default provider API key variables."""
        with open(ENV_FILE, "w", encoding="utf-8") as file:
            for key, value in DEFAULT_ENV.items():
                file.write(f"{key}={value}\n")

    def exists(self) -> bool:
        """Checks if the .env file exists."""
        return ENV_FILE.exists()

    def load(self) -> dict[str, str]:
        """Loads environment variables defined in the .env file."""
        return {k: v for k, v in dotenv_values(ENV_FILE).items() if v is not None}

    def save(self, env: dict[str, str]) -> None:
        """Saves environment variables to the .env file."""
        with open(ENV_FILE, "w", encoding="utf-8") as file:
            for key, value in env.items():
                val = value if value is not None else ""
                file.write(f"{key}={val}\n")

    def _resolve_provider(self, provider: str) -> ProviderMetadata:
        """
        Helper to resolve a provider string name to a ProviderMetadata object.
        Raises ProviderNotFoundError if the provider is unsupported.
        """
        provider_key = provider.lower().strip()
        if provider_key not in PROVIDERS:
            from forgeX.config.exceptions import ProviderNotFoundError
            raise ProviderNotFoundError(f"Unsupported provider: '{provider}'")
        return PROVIDERS[provider_key]

    def get_api_key(self, provider: str) -> str | None:
        """
        Gets the API key for a given provider. Resolves the key name internally.
        Checks the local .env first, falling back to system environment variables.
        """
        prov = self._resolve_provider(provider)
        if not prov.api_key_env:
            return None
        
        # 1. Load from local .env
        env = self.load()
        key_val = env.get(prov.api_key_env)
        if key_val and key_val.strip():
            return key_val.strip()
            
        # 2. Fall back to system environment
        sys_val = os.environ.get(prov.api_key_env)
        if sys_val and sys_val.strip():
            return sys_val.strip()
            
        return None

    def set_api_key(self, provider: str, api_key: str) -> None:
        """
        Sets the API key for a given provider in the .env file.
        Raises ValidationError if the provider does not require an API key.
        """
        prov = self._resolve_provider(provider)
        if not prov.api_key_env:
            from forgeX.config.exceptions import ValidationError
            raise ValidationError(f"Provider '{prov.display_name}' does not require/support an API key.")
        
        env = self.load()
        env[prov.api_key_env] = api_key.strip()
        self.save(env)

    def has_api_key(self, provider: str) -> bool:
        """Checks if a provider has an API key configured."""
        return bool(self.get_api_key(provider))

    def remove_api_key(self, provider: str) -> None:
        """Removes the API key configuration for a provider in the .env file."""
        prov = self._resolve_provider(provider)
        if not prov.api_key_env:
            return
        
        env = self.load()
        if prov.api_key_env in env:
            env[prov.api_key_env] = ""
            self.save(env)