from forgeX.config.constants import PROVIDERS
from forgeX.config.env_manager import EnvironmentManager
from forgeX.config.exceptions import (
    APIKeyMissingError,
    ModelNotFoundError,
    ProviderNotFoundError,
)
from forgeX.config.models import ForgeXConfig


class ConfigValidator:
    def __init__(self):
        self.env_manager = EnvironmentManager()

    def _validate_provider(self, config: ForgeXConfig):
        provider = config.llm.provider
        if not provider:
            raise ProviderNotFoundError("Provider not specified in the configuration.")
        if provider not in PROVIDERS:
            raise ProviderNotFoundError("Specified Provider not available")

    def _validate_model(self, config: ForgeXConfig):
        model = config.llm.model.strip()
        if not model:
            raise ModelNotFoundError("Model not specified in the configuration.")

    def _validate_api_key(self, config: ForgeXConfig):
        provider = config.llm.provider
        provider_info = PROVIDERS.get(provider)
        if provider_info.requires_api_key:
            if not self.env_manager.has_api_key(provider):
                raise APIKeyMissingError(
                    f"API key for provider '{provider}' not found in the environment."
                )
            return None
        return None

    def validate(self, config: ForgeXConfig):

        self._validate_provider(config)
        self._validate_model(config)

        self._validate_api_key(config)
