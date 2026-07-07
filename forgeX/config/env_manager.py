from dotenv import dotenv_values

from forgeX.config.constants import (
    CONFIG_DIR,
    DEFAULT_ENV,
    ENV_FILE,
    PROVIDERS,
)


class EnvironmentManager:
    def __init__(self):

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if not ENV_FILE.exists():
            self.create()

    def create(self) -> None:

        with open(ENV_FILE, "w", encoding="utf-8") as file:
            for key, value in DEFAULT_ENV.items():
                file.write(f"{key}={value}\n")

    def exists(self) -> bool:

        return ENV_FILE.exists()

    def load(self) -> dict:

        return dict(dotenv_values(ENV_FILE))

    def save(self, env: dict) -> None:

        with open(ENV_FILE, "w", encoding="utf-8") as file:
            for key, value in env.items():
                if value is None:
                    value = ""

                file.write(f"{key}={value}\n")

    def get_api_key(self, provider: str) -> str | None:

        provider = provider.lower()

        provider_info = PROVIDERS.get(provider)

        if provider_info is None:
            raise ValueError(f"Unsupported provider: {provider}")

        env_key = provider_info.api_key_env

        if env_key is None:
            return None

        env = self.load()

        return env.get(env_key)

    def set_api_key(self, provider: str, api_key: str) -> None:

        provider = provider.lower()

        provider_info = PROVIDERS.get(provider)

        if provider_info is None:
            raise ValueError(f"Unsupported provider: {provider}")

        env_key = provider_info.api_key_env

        if env_key is None:
            raise ValueError(f"{provider} does not use an API key.")

        env = self.load()

        env[env_key] = api_key

        self.save(env)

    def has_api_key(self, provider: str) -> bool:

        key = self.get_api_key(provider)

        return bool(key)

    def remove_api_key(self, provider: str) -> None:

        provider = provider.lower()

        provider_info = PROVIDERS.get(provider)

        if provider_info is None:
            raise ValueError(f"Unsupported provider: {provider}")

        env_key = provider_info.api_key_env

        if env_key is None:
            return

        env = self.load()

        env[env_key] = ""

        self.save(env)
