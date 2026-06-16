from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Literal


class QuickOption(str, Enum):
    """List of choices for quick information gathering."""

    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    AUTO = "auto"

AvailableQuickOption = Literal["summary","contacts","products","auto"]

class UrlExtractionRequest(BaseModel):
    """
    The setup information sent by a user to start reading a website.

    This model holds the website link, what information to look for, 
    and settings for how long to try reading the page before giving up.

    Attributes:
        source: The link to the website you want to read.
        prompt: Your own written instructions on what to extract.
        quick_option: A ready-made choice for quick information gathering.
        llm_timeout: How many seconds to wait for the AI to answer.
        llm_retry: How many times to try asking the AI again if it fails.
        crawl_timeout: How many seconds to wait for the webpage to load.
        crawl_retry: How many times to try loading the webpage again if it fails.
        response_schema: A custom format provided by the user to organize the final output.
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
    response_schema: type[BaseModel] | None = Field(
        None,
        description="A custom format provided by the user to organize the final output."
    )