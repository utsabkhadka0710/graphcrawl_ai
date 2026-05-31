from pydantic import BaseModel
from enum import Enum

class QuickOptions(Enum):
    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    AUTO = "auto"


class ExtractionRequest(BaseModel):
    """
    Represents extraction request made by user

    This is a model representation of what user requestse even before it hits the fetcher
    includes the source and prompt/quick extraction(pre defined extraction options)
    """
    source: str
    prompt: str | None = None
    quick_extraction: QuickOptions | None = None


