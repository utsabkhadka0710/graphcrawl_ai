from pydantic import BaseModel
from enum import Enum

class QuickOption(str, Enum):
    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    AUTO = "auto"

class ExtractionRequestByUser(BaseModel):
    """
    Represents extraction request made by user

    This model is a representation of what user requests even before it hits the fetcher
    includes the source and prompt/quick extraction(pre defined extraction options) 
    """
    source: str
    prompt: str | None = None
    quick_option: QuickOption | None = None


class ExtractionRequestToLLM(BaseModel):
    """
    Represents extraction request being sent to LLM for scraping from url

    This model is a representation of the actual thing LLM needs to actually scrape
     - content (which is clean text parsed from HTML fetched from the requsted url.)
     - prompt (prompt that guides LLM for scraping as per user requirement.)
    """
    content: str
    prompt: str

