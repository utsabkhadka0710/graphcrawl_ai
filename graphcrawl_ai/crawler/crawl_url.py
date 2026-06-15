from graphcrawl_ai.llm.request_resolver.user_url_request_resolver import resolve_url_request
from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest, AvailableQuickOption
from graphcrawl_ai.llm.gemini_extractor import get_response_gemini
from typing import Literal, Optional, TypeVar, get_args
from pydantic import BaseModel, ValidationError

# Exceptions imports
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import(
    UrlMissingError,
    PromptMissingError
)


CrawlUrlResponse = TypeVar("ResponseSchema",bound=BaseModel)

def crawl_url(source: str = None,
              prompt: str = None, 
              quick_option: AvailableQuickOption = None, 
              llm_timeout: Optional[float] = 60,
              llm_retry: Optional[float] = 3,
              crawl_timeout: Optional[float] = 30, 
              crawl_retry: Optional[float] = 3,
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
    
    if source is None or str(source).strip() == "":
        raise UrlMissingError

    if (prompt is None or str(prompt).strip() == "" ) and (quick_option is None or str(quick_option).strip() == ""):
            raise PromptMissingError
    
    timeout_and_retry_params = (llm_timeout, llm_retry, crawl_timeout, crawl_retry)
    if all(isinstance(param, str) and not param.isdigit() for param in timeout_and_retry_params):
         raise
    
    request_by_user: UrlExtractionRequest = None
    from math import ceil
    request_by_user = UrlExtractionRequest(
        source = source,
        prompt = prompt,
        quick_option = quick_option,
        llm_timeout = ceil(float(llm_timeout)),
        llm_retry = ceil(float(llm_retry)),
        crawl_timeout = ceil(float(crawl_timeout)),
        crawl_retry = ceil(float(crawl_retry)),
        response_schema = response_schema
    )


    request_to_llm, response_schema = resolve_url_request(request=request_by_user)
    
    response_from_llm = get_response_gemini(request=request_to_llm, response_schema=response_schema)

    return response_from_llm