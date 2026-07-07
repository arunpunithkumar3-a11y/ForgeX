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


# ============================================================================
# Root Configuration
# ============================================================================


@dataclass(slots=True)
class ForgeXConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
