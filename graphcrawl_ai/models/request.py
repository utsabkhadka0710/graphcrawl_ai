from pydantic import BaseModel, model_validator
from enum import Enum
from graphcrawl_ai.llm import prompts

class QuickOption(str, Enum):
    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    AUTO = "auto"

    @property
    def option(self) -> str:
        if self == QuickOption.SUMMARY:
            return prompts.summary
        if self == QuickOption.CONTACTS:
            return prompts.contacts
        if self == QuickOption.PRODUCTS:
            return prompts.products
        if self == QuickOption.AUTO:
            return prompts.auto

class ExtractionRequest(BaseModel):
    """
    Represents extraction request made by user

    This is a model representation of what user requestse even before it hits the fetcher
    includes the source and prompt/quick extraction(pre defined extraction options) 
    """
    source: str
    prompt: str | None = None
    quick_option: QuickOption | None = None

    @model_validator(mode="after")
    def get_prompt_from_option(self) -> ExtractionRequest:
        
        if self.prompt and self.quick_option:
            self.quick_option = None

        if self.quick_option and not self.prompt:
            self.prompt = self.quick_option.option

        return self
