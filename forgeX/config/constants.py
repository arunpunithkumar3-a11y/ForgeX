from pathlib import Path
from platformdirs import user_config_dir
from forgeX.config.models import ProviderMetadata

APP_NAME = "ForgeX"

CONFIG_DIR = Path(user_config_dir(APP_NAME, appauthor=False))
CONFIG_FILE = CONFIG_DIR / "config.toml"
ENV_FILE = CONFIG_DIR / ".env"

# ============================================================================
# Supported Providers Registry
# ============================================================================
PROVIDERS: dict[str, ProviderMetadata] = {
    "openrouter": ProviderMetadata(
        name="openrouter",
        display_name="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        requires_api_key=True,
        base_url_env="OPENROUTER_BASE_URL",
    ),
    "openai": ProviderMetadata(
        name="openai",
        display_name="OpenAI",
        api_key_env="OPENAI_API_KEY",
        requires_api_key=True,
        base_url_env="OPENAI_BASE_URL",
    ),
    "anthropic": ProviderMetadata(
        name="anthropic",
        display_name="Anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        requires_api_key=True,
        base_url_env="ANTHROPIC_BASE_URL",
    ),
    "gemini": ProviderMetadata(
        name="gemini",
        display_name="Google Gemini",
        api_key_env="GEMINI_API_KEY",
        requires_api_key=True,
        base_url_env="GEMINI_BASE_URL",
    ),
    "groq": ProviderMetadata(
        name="groq",
        display_name="Groq",
        api_key_env="GROQ_API_KEY",
        requires_api_key=True,
        base_url_env="GROQ_BASE_URL",
    ),
    "nvidia": ProviderMetadata(
        name="nvidia",
        display_name="NVIDIA",
        api_key_env="NVIDIA_API_KEY",
        requires_api_key=True,
        base_url_env="NVIDIA_BASE_URL",
    ),
    "ollama": ProviderMetadata(
        name="ollama",
        display_name="Ollama",
        api_key_env=None,
        requires_api_key=False,
        base_url_env="OLLAMA_HOST",
    ),
}

# Default configuration dictionary used to initialize config.toml
DEFAULT_CONFIG = {
    "llm": {
        "provider": "openai",
        "model": "gpt-4o",
    },
    "generation": {
        "temperature": 0.2,
        "max_tokens": 4096,
    }
}

# Default environment variables dict generated from PROVIDERS
DEFAULT_ENV = {
    prov.api_key_env: ""
    for prov in PROVIDERS.values()
    if prov.api_key_env is not None
}
