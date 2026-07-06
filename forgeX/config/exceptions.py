class ForgeXConfigError(Exception):
    """Base exception class for all configuration errors in ForgeX."""
    pass

class ProviderNotFoundError(ForgeXConfigError):
    """Raised when a specified provider is not found or is unsupported."""
    pass

class ModelNotFoundError(ForgeXConfigError):
    """Raised when a specified model is invalid or missing."""
    pass

class APIKeyMissingError(ForgeXConfigError):
    """Raised when a provider requires an API key but none is found."""
    pass

class ValidationError(ForgeXConfigError):
    """Raised when configuration integrity checks fail."""
    pass
