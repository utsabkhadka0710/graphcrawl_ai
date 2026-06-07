from pydantic import BaseModel, Field
from typing import Optional


class ExtractionRequestToLLM(BaseModel):
    """
    Represents the internal request payload formatted for the LLM.

    This model acts as the final schema passed to the extraction engine. 
    It contains only the prepared data ready for LLM processing.

    Attributes:
        content: The cleaned and parsed text content extracted from the URL.
        prompt: The fully resolved prompt instruction to guide the LLM extraction.
        llm_timeout: Maximum time in seconds to wait for the LLM to finish.
        llm_retry: Number of times to try again if the LLM request fails.
    """

    __module__ = "graphcrawl_ai"

    content: str = Field(
        ..., 
        description="The cleaned and parsed text content extracted from the URL."
    )
    prompt: str = Field(
        ..., 
        description="The fully resolved prompt instruction to guide the LLM extraction."
    )
    llm_timeout: Optional[float] = Field(
        60, 
        description="Maximum time in seconds to wait for the LLM to finish."
    )
    llm_retry: Optional[float] = Field(
        3, 
        description="Number of times to try again if the LLM request fails."
    )