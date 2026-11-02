from pydantic import BaseModel, Field, HttpUrl, model_validator
from enum import Enum
from typing import Optional, Literal

from graphcrawl_ai.llm.prompts import summary, contacts, products
from graphcrawl_ai.models.crawl_url.response_models.llm_response import(
    UrlSummaryResponse,
    UrlContactsResponse,
    UrlProductsResponse
)

class QuickOption(str, Enum):
    """List of choices for quick information gathering."""

    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"

AvailableQuickOption = Literal["summary","contacts","products"]

class ConfigLLM(BaseModel):
    """A placeholder configuration template for controlling the AI model.

    This model is currently under development and will be used to manage internal 
    AI routing properties like names, API targets, and schema layouts.
    """
    model: str
    api: str
    response_model: type[BaseModel]
    

class UrlExtractionRequest(BaseModel):
    """
    The setup information sent by a user to start reading a website.

    This model holds the website link, what information to look for, 
    which AI provider to use, and settings for timing and retry preferences.

    Attributes:
        source: The link to the website you want to read.
        prompt: Your own written instructions on what to extract.
        quick_option: A ready-made choice for quick information gathering.
        model: The specific name of the AI model to run.
        api_key: The secret password or key needed to access the AI provider.
        response_schema: A custom format provided by the user to organize the final output.
        llm_timeout: How many seconds to wait for the AI to answer.
        llm_retry: How many times to try asking the AI again if it fails.
        crawl_timeout: How many seconds to wait for the webpage to load.
        crawl_retry: How many times to try loading the webpage again if it fails.
    """

    __module__ = "graphcrawl_ai"

    source: HttpUrl = Field(
        ...,
        description="The link to the website you want to read.",
        strict=True
    )
    prompt: str | None = Field(
        None,
        description="Your own written instructions on what to extract."
    )
    quick_option: QuickOption | None = Field(
        None,
        description="A ready-made choice for quick information gathering."
    )
    model: str = Field(
        ...,
        description="LLM model used for extraction"
    )
    api_key: Optional[str] = Field(
        None,
        description="api key of the model"
    )
    response_schema: type[BaseModel] | None = Field(
        None,
        description="A custom format provided by the user to organize the final output."
    )
    llm_timeout: Optional[int] = Field(
        30,
        description="How many seconds to wait for the AI to answer."
    )
    llm_retry: Optional[int] = Field(
        3,
        description="How many times to try asking the AI again if it fails."
    )
    crawl_timeout: Optional[int] = Field(
        30,
        description="How many seconds to wait for the webpage to load."
    )
    crawl_retry: Optional[int] = Field(
        3,
        description="How many times to try loading the webpage again if it fails."
    )

      
    @model_validator(mode='after')
    def resolve_quick_option_and_prompt(self):
        if not self.quick_option and not self.prompt:
            raise ValueError(
                "Either 'quick_option' or 'prompt' is needed but both are missing, "
                "please select one of the availabe quick_option or provide a custom prompt."
            )
        if self.quick_option and not self.prompt:
            match self.quick_option:
                case QuickOption.SUMMARY:
                    self.prompt = summary
                    self.response_schema = UrlSummaryResponse
                case QuickOption.CONTACTS:
                    self.prompt = contacts
                    self.response_schema = UrlContactsResponse
                case QuickOption.PRODUCTS:
                    self.prompt = products
                    self.response_schema = UrlProductsResponse
        if self.prompt:
            if not self.response_schema:
                raise ValueError(
                    "'response_schema' missing! "
                    "a custom prompt was given which requires custom response schema, "
                    "please provide a 'response_shema' and try again."
                )
            self.prompt = self.prompt
            self.response_schema = self.response_schema
        return self
