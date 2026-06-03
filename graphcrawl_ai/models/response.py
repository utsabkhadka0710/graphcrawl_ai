from pydantic import BaseModel, Field

class ParsedContent(BaseModel):
    """
    Represent structured content extracted from raw HTML.

    Produced by HTML parsing stage and contains
    metadata 'title' and cleaned extracted from a page(HTML).
    """
    title: str = Field(..., description="Title of the HTML")
    content: str = Field(..., description="Extracted clean text from HTML")