from graphcrawl_ai.resolver.url_resolver import resolve_url_request
from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest, AvailableQuickOption
from graphcrawl_ai.llm.engine import llm_extract
from typing import Optional, TypeVar
from pydantic import BaseModel, ValidationError

# Exceptions imports
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import InvalidDataError


CrawlUrlResponse = TypeVar("ResponseSchema",bound=BaseModel)

async def crawl_url(
    source: str | None = None,
    prompt: str | None = None, 
    quick_option: AvailableQuickOption | None = None,
    model: str | None = None,
    api_key: str | None = None,
    response_schema: type[BaseModel] | None = None,
    llm_timeout: Optional[float] = 60,
    llm_retry: Optional[float] = 3,
    crawl_timeout: Optional[float] = 30, 
    crawl_retry: Optional[float] = 3
) -> CrawlUrlResponse:
    """Read a webpage and pull out specific information using an AI model.

    This function coordinates the whole process: it double-checks your inputs, 
    downloads the website text, selects the right instructions, and asks the AI 
    engine to format everything into your final organized answer.

    Args:
        source: The link to the website you want to read.
        prompt: Your own written instructions on what to look for.
        quick_option: A ready-made choice like summary, contacts, or products.
        model: The specific name of the AI model to run.
        api_key: The secret password or key needed to access the AI provider.
        response_schema: A custom format model if you want the output in a specific layout.
        llm_timeout: How many seconds to wait for the AI to answer.
        llm_retry: How many times to try asking the AI again if it fails.
        crawl_timeout: How many seconds to wait for the webpage to load.
        crawl_retry: How many times to try loading the webpage again if it fails.

    Returns:
        An object holding the final organized answers found on the website.

    Raises:
        UrlMissingError: If you forget to provide a website link.
        PromptMissingError: If you forget to provide either a custom prompt 
            or a quick option selection.
        ResponseSchemaMissingError: If you provide custom instructions but forget 
            to supply a template model layout to format the answer into.
        InvalidDataError: If any of your setting options or numbers are set incorrectly.
    """
     
    request_by_user: UrlExtractionRequest = None

    try:
        request_by_user = UrlExtractionRequest(
            source=source,
            prompt=prompt,
            quick_option=quick_option,
            model=model,
            api_key=api_key,
            response_schema=response_schema,
            llm_timeout=llm_timeout,
            llm_retry=llm_retry,
            crawl_timeout=crawl_timeout,
            crawl_retry=crawl_retry,
        )
    except ValidationError as e:
        err_msg = e.errors()
        failed_param = err_msg[0]["loc"][0]
        failed_msg = err_msg[0]["msg"]
        raise InvalidDataError(param_name=failed_param, message=failed_msg)
    
    request_to_llm = await resolve_url_request(request=request_by_user)
    
    response_from_llm = await llm_extract(request=request_to_llm)

    return response_from_llm