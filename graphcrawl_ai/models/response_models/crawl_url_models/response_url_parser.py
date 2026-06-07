from pydantic import BaseModel, Field
from typing import Literal, Optional


class HtmlParsedContent(BaseModel):
    """
    Represents structured content extracted from raw HTML.

    This model is produced by the internal HTML parsing stage. It acts as the 
    sanitized intermediate payload containing clean textual data and page metadata 
    before LLM processing.

    Attributes:
        title: Title of the HTML page.
        content: Extracted clean text from HTML.
    """

    __module__ = "graphcrawl_ai"

    title: str = Field(
        ...,
        description="The extracted title of the source HTML page."
    )
    content: str = Field(
        ...,
        description="The cleaned, raw text content parsed from the HTML body."
    )
