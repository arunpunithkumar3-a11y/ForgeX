import os
from pathlib import Path
from dotenv import load_dotenv


from langchain_core.output_parsers import PydanticOutputParser
from testing import llm
from forgeX.tools.Terminal.security.models import CommandRequest, ValidationResult
from forgeX.tools.Terminal.security.prompts import security_prompt

class SecurityManager:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=ValidationResult)
        self.chain = security_prompt | llm | self.parser

    def validate(self, config: CommandRequest) -> ValidationResult:
        try:
            input_data = {
                "command":str(config.command),
                "cwd": str(config.cwd),
                "workspace": str(config.workspace),
                "timeout": config.timeout
            }
            response = self.chain.invoke(input_data)
            return response
        except Exception as e:
            return ValidationResult(
                allowed=False,
                risk="critical",
                reason=f"Validation failed with error: {str(e)}"
            )



        