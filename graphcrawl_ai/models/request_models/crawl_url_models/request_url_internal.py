from pydantic import BaseModel, Field


class ExtractionRequestToLLM(BaseModel):
    """
    Represents the internal request payload formatted for the LLM.

    This model serves as the final schema passed to the core extraction engine. 
    It abstracts away user-facing selection logic by containing only the raw, 
    fetched content and the fully resolved prompt instruction.

    Attributes:
        content: The cleaned, raw text content parsed from the target URL's HTML.
        prompt: The finalized natural language instruction guiding the LLM 
            (either custom-written by the user or mapped from a QuickOption).
    """
    content: str = Field(..., description="The cleaned and parsed text content extracted from the URL.")
    prompt: str = Field(..., description="The fully resolved prompt instruction to guide the LLM extraction.")