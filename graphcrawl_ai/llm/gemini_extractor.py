import os, math
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import TypeVar
from pydantic import BaseModel
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_llm import ExtractionRequestToLLM

ResponseSchema = TypeVar("T", bound=BaseModel)

load_dotenv()

llm_api = str(os.getenv("GEMINI_API"))

def get_response_gemini(request: ExtractionRequestToLLM, response_schema: type[ResponseSchema]) -> ResponseSchema:
    """Send the cleaned website text to the Gemini AI to extract the data.

    This function sets up the connection to the Gemini AI service, configures
    how long to wait for an answer, and decides how many times to retry if 
    something goes wrong. It then tells the AI what to look for and turns the 
    AI's final text answer into an organized data object.

    Args:
        request: An object holding the website text, the instructions, 
            and time or retry settings for the AI.
        response_schema: The data layout template used to shape and check 
            the final answer.

    Returns:
        An organized data object that matches the requested layout template.

    Note:
        This function requires a valid Gemini API key to be saved in your 
        environment setup variables under the name 'GEMINI_API'.
    """
    
    content = request.content
    prompt = request.prompt

    http_config = types.HttpOptions(
        timeout=int(math.ceil(request.llm_timeout)*1000),
        retry_options = types.HttpRetryOptions(
            attempts = request.llm_retry,
            initial_delay = 5.0,
            max_delay = 60.0,
            http_status_codes = [408, 429, 500, 503]
        )

    )

    client = genai.Client(api_key=llm_api, http_options=http_config)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=content,
        config=types.GenerateContentConfig(
            system_instruction = prompt,
            response_mime_type = "application/json",
            response_schema = response_schema,
        )
    )

    llm_response = response.text
    llm_schema_response = response_schema.model_validate_json(llm_response)

    return llm_schema_response