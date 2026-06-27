from pydantic import BaseModel, Field, ConfigDict
from abc import ABC
from typing import Literal, Optional


class UrlBaseResponse(BaseModel, ABC):
    """
    The main starting point for answers sent back by the AI.

    This model forms the base for all specific types of answers, 
    making sure every response includes a clear status showing if it worked.

    Attributes:
        status: Shows if the task finished successfully or failed.
    """
    __module__ = "graphcrawl_ai"

    status: Literal["success", "failure"] = Field(
        ..., 
        description="Shows if the task finished successfully or failed."
    )


class UrlPromptResponse(UrlBaseResponse):
    """
    The answer generated from your own custom instructions.

    This model holds a list of text details found on the website 
    based on the specific questions you asked.

    Attributes:
        response: A list of text answers found based on your instructions.
    """

    __module__ = "graphcrawl_ai"

    response: list[str] = Field(
        ..., 
        description="A list of text answers found based on your instructions."
    )


class UrlSummaryResponse(UrlBaseResponse):
    """
    A short overview of the website text.

    This model gives you a quick description of the webpage along 
    with a list of the most important points.

    Attributes:
        summary: A short description of what is on the website.
        key_takeaways: A list of the most important points found in the text.
    """

    __module__ = "graphcrawl_ai"

    summary: str = Field(
        ..., 
        description="A short description of what is on the website."
    )
    key_takeaways: list[str] = Field(
        ..., 
        description="A list of the most important points found in the text."
    )


class ContactsList(BaseModel):
    """
    A list of different ways to get in touch with someone.

    This model groups together basic contact details found on a page, 
    like phone numbers, links, and addresses.

    Attributes:
        emails: A list of email addresses.
        phones: A list of phone numbers.
        addresses: A list of physical mail addresses.
        social_links: A list of social media links.
    """
    emails: list[str] = Field(default_factory=list, description="A list of email addresses.")
    phones: list[str] = Field(default_factory=list, description="A list of phone numbers.")
    addresses: list[str] = Field(default_factory=list, description="A list of physical mail addresses.")
    social_links: list[str] = Field(default_factory=list, description="A list of social media links.")


class UrlContactsResponse(UrlBaseResponse):
    """
    The answer containing contact details found on the website.

    This model gathers and organizes all the communication channels 
    found during the search.

    Attributes:
        contact_info: The grouped contact details like emails, phone numbers, and addresses.
    """

    __module__ = "graphcrawl_ai"

    contact_info: ContactsList = Field(
        ..., 
        description="The grouped contact details like emails, phone numbers, and addresses."
    )


class ProductItem(BaseModel):
    """
    The details for a single item found on a store page.

    This model holds standard store information for an item, such as 
    what it costs, its name, and its rating.

    Attributes:
        name: The name of the item.
        price: How much the item costs.
        description: A short description of the item.
        rating: The score or reviews given to the item.
        total_sold: How many times this item has been bought.
    """

    __module__ = "graphcrawl_ai"

    name: str = Field(..., description="The name of the item.")
    price: str = Field(..., description="How much the item costs.")
    description: str = Field(..., description="A short description of the item.")
    rating: str = Field(..., description="The score or reviews given to the item.")
    total_sold: str = Field(..., description="How many times this item has been bought.")


class UrlProductsResponse(UrlBaseResponse):
    """
    The answer containing a list of items found on a website.

    This model tells you if any items were discovered on the page 
    and lists their details.

    Attributes:
        products_found: True if items were found on the page, False if not.
        products: A list containing the details of each item found.
    """

    __module__ = "graphcrawl_ai"

    products_found: bool = Field(
        ..., 
        description="True if items were found on the page, False if not."
    )
    products: list[ProductItem] = Field(
        ..., 
        description="A list containing the details of each item found."
    )