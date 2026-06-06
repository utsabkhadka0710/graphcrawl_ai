from pydantic import BaseModel, Field
from enum import Enum


class QuickOption(str, Enum):
    """
    Enumeration of predefined quick extraction shortcuts.

    Provides users with pre-configured crawling strategies, eliminating the 
    need to manually compose a custom prompt for common extraction use cases.
    """
    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    AUTO = "auto"

class UrlExtractionRequestByUser(BaseModel):
    """
    Represents the raw extraction request submitted by the user.

    This model serves as the initial landing schema for the `crawl_url()` endpoint. 
    It captures and validates user inputs before the target URL is fetched or the 
    prompt logic is resolved.

    Attributes:
        source: The target URL string to be crawled and scraped.
        prompt: A custom natural language instruction for tailored extraction. 
            Optional if a `quick_option` is selected.
        quick_option: A shortcut strategy mode. Mutually exclusive with `prompt` 
            in terms of application logic, but optional in the schema.
    """
    source: str = Field(..., description="The target URL to crawl and scrape.")
    prompt: str | None = Field(None, description="Custom text instructions for the extraction.")
    quick_option: QuickOption | None = Field(None, description="Predefined shortcut mode for quick crawling.")