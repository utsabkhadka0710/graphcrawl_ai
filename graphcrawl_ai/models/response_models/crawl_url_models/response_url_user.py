from pydantic import BaseModel, Field


class URLExtractionResponseToUser(BaseModel):
    """
    Represents the final structured response returned to the user.

    This model acts as the final output schema for the `crawl_url()` endpoint,
    delivering the successfully extracted data back to the client after LLM 
    processing and validation.

    Attributes:
        response_to_user: A dynamic dictionary containing the structured key-value 
            pairs extracted by the LLM based on the user's criteria.
    """
    response_to_user: dict = Field(..., description="The final structured data extracted by the LLM, formatted as a dictionary.")