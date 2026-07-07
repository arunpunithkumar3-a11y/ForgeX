import tomlkit

from forgeX.config.constants import (
    CONFIG_DIR,
    CONFIG_FILE,
    DEFAULT_CONFIG,
)
from forgeX.config.models import (
    ForgeXConfig,
    LLMConfig,
)


class ConfigManager:
    def __init__(self):

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if not CONFIG_FILE.exists():
            self.create()

    def create(self) -> None:

        document = tomlkit.document()

        document.update(DEFAULT_CONFIG)

        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            tomlkit.dump(document, file)

    def exists(self) -> bool:

        return CONFIG_FILE.exists()

    def load(self) -> ForgeXConfig:

        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            data = tomlkit.load(file)

        return ForgeXConfig(
            llm=LLMConfig(
                provider=data["llm"]["provider"],
                model=data["llm"]["model"],
            ),
        )

    def save(self, config: ForgeXConfig) -> None:

        document = tomlkit.document()

        document["llm"] = {
            "provider": config.llm.provider,
            "model": config.llm.model,
        }

        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            tomlkit.dump(document, file)

    def reset(self) -> None:

        self.create()
