from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Literal


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

    source: str = Field(
        ...,
        description="The link to the website you want to read."
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