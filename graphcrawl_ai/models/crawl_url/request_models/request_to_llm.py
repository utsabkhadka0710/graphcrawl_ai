from pydantic import BaseModel, Field
from typing import Optional


class ExtractionJobToLLM(BaseModel):
    """
    The final data package sent to the AI for processing.

    This model collects the clean webpage text, the specific instructions 
    on what to find, the layout template for the answer, and the timing 
    or retry rules before calling the AI engine.

    Attributes:
        content: The cleaned and parsed text content extracted from the URL.
        prompt: The final instructions telling the AI what to look for.
        model: The specific name of the AI model to run.
        api_key: The secret password or key needed to access the AI provider.
        response_schema: The template model used to shape and format the AI's answer.
        llm_timeout: How many seconds to wait for the AI to answer.
        llm_retry: How many times to try asking the AI again if it fails.
    """

    __module__ = "graphcrawl_ai"

    content: str = Field(
        ..., 
        description="The cleaned and parsed text content extracted from the URL."
    )
    prompt: str = Field(
        ..., 
        description="The final instructions telling the AI what to look for."
    )
    model: str = Field(
        ...,
        description="LLM model used for extraction"
    )
    api_key: Optional[str] = Field(
        None,
        description="api key of the model"
    )
    response_schema: type[BaseModel] = Field(
        ...,
        description="The template model used to shape and format the AI's answer."
    )
    llm_timeout: Optional[int] = Field(
        60, 
        description="How many seconds to wait for the AI to answer."
    )
    llm_retry: Optional[int] = Field(
        3, 
        description="How many times to try asking the AI again if it fails."
    )