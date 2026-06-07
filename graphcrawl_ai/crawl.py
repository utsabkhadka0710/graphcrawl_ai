from graphcrawl_ai.llm.request_resolver.user_url_request_resolver import resolve_url_request
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_user import UrlExtractionRequest
from graphcrawl_ai.llm.gemini_extractor import get_response_gemini
from typing import Literal, Optional, TypeVar
from pydantic import BaseModel

from graphcrawl_ai.models.response_models.crawl_url_models.response_url_llm import (
    UrlPromptResponse,
    UrlSummaryResponse,
    UrlContactsResponse,
    UrlProductsResponse,
    UrlAutoResponse
)

CrawlUrlResponse = TypeVar("T", bound=BaseModel)

def crawl_url(source: str,
              prompt: str = None, 
              quick_option: Literal["summary","contacts","products","auto"] = None, 
              llm_timeout: Optional[float] = 60,
              llm_retry: Optional[int] = 3,
              timeout: Optional[float] = 30, 
              retry: Optional[int] = 3,
              response_schema: type[CrawlUrlResponse] | None = None 
            ) -> CrawlUrlResponse:
    """Read a website and extract specific information from it using AI.

    This function coordinates the whole process: it loads the requested website, 
    cleans up the text, picks the right instructions or template, and sends everything 
    to the AI engine to get your final organized answer.

    Args:
        source: The link to the website you want to read.
        prompt: Your own written instructions on what to look for.
        quick_option: A ready-made choice like summary, contacts, products, or auto.
        llm_timeout: How many seconds to wait for the AI to answer.
        llm_retry: How many times to try asking the AI again if it fails.
        timeout: How many seconds to wait for the webpage to load.
        retry: How many times to try loading the webpage again if it fails.
        response_schema: A custom format model if you want the output in a specific layout.

    Returns:
        An object holding the final organized answers found on the website.

    Note:
        You need to give either a custom prompt or choose a quick option so the 
        system knows what information you are looking for.
    """
    
    request_by_user = UrlExtractionRequest(
        source = source,
        prompt = prompt,
        quick_option = quick_option,
        llm_timeout = llm_timeout,
        llm_retry = llm_retry,
        crawl_timeout = timeout,
        crawl_retry = retry,
        response_schema = response_schema
    )

    request_to_llm, response_schema = resolve_url_request(request=request_by_user)
    
    response_from_llm = get_response_gemini(request=request_to_llm, response_schema=response_schema)

    return response_from_llm