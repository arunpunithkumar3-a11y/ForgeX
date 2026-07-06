from dataclasses import dataclass, field


# ============================================================================
# Provider Metadata
# ============================================================================

@dataclass(slots=True, frozen=True)
class ProviderMetadata:
    name: str
    display_name: str
    api_key_env: str | None
    requires_api_key: bool
    base_url_env: str | None


# ============================================================================
# LLM Configuration
# ============================================================================

@dataclass(slots=True)
class LLMConfig:
    provider: str = ""
    model: str = ""


# ============================================================================
# Generation Configuration
# ============================================================================

@dataclass(slots=True)
class GenerationConfig:
    temperature: float = 0.2
    max_tokens: int = 4096


# ============================================================================
# Root Configuration
# ============================================================================

@dataclass(slots=True)
class ForgeXConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)