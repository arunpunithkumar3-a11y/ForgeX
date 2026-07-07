from pathlib import Path

from platformdirs import user_config_dir

from forgeX.config.models import ProviderMetadata

# ============================================================================
# Application
# ============================================================================

APP_NAME: str = "ForgeX"


# ============================================================================
# Directories
# ============================================================================

CONFIG_DIR: Path = Path(user_config_dir(APP_NAME))

CONFIG_FILE: Path = CONFIG_DIR / "config.toml"

ENV_FILE: Path = CONFIG_DIR / ".env"

LOGS_DIR: Path = CONFIG_DIR / "logs"

CACHE_DIR: Path = CONFIG_DIR / "cache"

HISTORY_DB: Path = CONFIG_DIR / "history.db"


# ============================================================================
# Provider Metadata
# ============================================================================

PROVIDERS = {
    "openrouter": ProviderMetadata(
        name="openrouter",
        display_name="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        requires_api_key=True,
        base_url_env=None,
    ),
    "openai": ProviderMetadata(
        name="openai",
        display_name="OpenAI",
        api_key_env="OPENAI_API_KEY",
        requires_api_key=True,
        base_url_env=None,
    ),
    "anthropic": ProviderMetadata(
        name="anthropic",
        display_name="Anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        requires_api_key=True,
        base_url_env=None,
    ),
    "google": ProviderMetadata(
        name="google",
        display_name="Google Gemini",
        api_key_env="GOOGLE_API_KEY",
        requires_api_key=True,
        base_url_env=None,
    ),
    "groq": ProviderMetadata(
        name="groq",
        display_name="Groq",
        api_key_env="GROQ_API_KEY",
        requires_api_key=True,
        base_url_env=None,
    ),
    "nvidia": ProviderMetadata(
        name="nvidia",
        display_name="NVIDIA",
        api_key_env="NVIDIA_API_KEY",
        requires_api_key=True,
        base_url_env=None,
    ),
    "ollama": ProviderMetadata(
        name="ollama",
        display_name="Ollama",
        api_key_env=None,
        requires_api_key=False,
        base_url_env="OLLAMA_BASE_URL",
    ),
}

SUPPORTED_PROVIDERS: tuple[str, ...] = tuple(PROVIDERS.keys())


# ============================================================================
# Default Configuration
# ============================================================================

DEFAULT_CONFIG = {
    "llm": {
        "provider": "",
        "model": "",
    },
    "generation": {
        "temperature": 0.2,
        "max_tokens": 4096,
    },
}


# ============================================================================
# Default Environment
# ============================================================================

DEFAULT_ENV = {
    "OPENROUTER_API_KEY": "",
    "OPENAI_API_KEY": "",
    "ANTHROPIC_API_KEY": "",
    "GOOGLE_API_KEY": "",
    "GROQ_API_KEY": "",
    "NVIDIA_API_KEY": "",
    "OLLAMA_BASE_URL": "http://localhost:11434",
}
