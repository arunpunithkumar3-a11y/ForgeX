from forgeX.config.manager import ConfigManager
from forgeX.config.env_manager import EnvironmentManager
from forgeX.config.models import ForgeXConfig
from forgeX.config.exceptions import *
from forgeX.config.constants import PROVIDERS
class ConfigValidator:
    def __init__(self):
        self.env_manager = EnvironmentManager()

    def _validate_provider(self,config:ForgeXConfig):
            provider = config.llm.provider
            if not provider:
                raise ProviderNotFoundError("Provider not specified in the configuration.")
            if provider not in PROVIDERS:
                raise ProviderNotFoundError("Specified Provider not available") 
   

    def _validate_model(self,config:ForgeXConfig):
            model = config.llm.model.strip()
            if not model:
                raise ModelNotFoundError("Model not specified in the configuration.")  


    def _validate_generation(self,config:ForgeXConfig):
        generation = config.generation
        if not generation:
            raise ValidationError("generation not specified in the configuration.")
        if not isinstance(generation.temperature,float)or not(0<=generation.temperature<=2):
            raise ValidationError("Temperature must be a float between 0 and 2.")  
        if not isinstance(generation.max_tokens,int) or  generation.max_tokens<=0:
            raise ValidationError("Max tokens must be a positive integer.")     
    def _validate_api_key(self,config:ForgeXConfig):
        provider = config.llm.provider
        provider_info = PROVIDERS.get(provider)
        if provider_info.requires_api_key:
            if not self.env_manager.has_api_key(provider):
                raise APIKeyMissingError(f"API key for provider '{provider}' not found in the environment.")
            return None
        return None   
     
    def validate(self,config:ForgeXConfig):
  
         self._validate_provider(config)
         self._validate_model(config)
         self._validate_generation(config)
         self._validate_api_key(config)
        





