from graphcrawl_ai.resolver.url_resolver import resolve_url_request
from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest, AvailableQuickOption
from graphcrawl_ai.llm.engine import llm_extract
from typing import Literal, Optional, TypeVar, get_args
from pydantic import BaseModel, ValidationError

# Exceptions imports
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import(
    UrlMissingError,
    PromptMissingError,
    InvalidDataError
)


CrawlUrlResponse = TypeVar("ResponseSchema",bound=BaseModel)

def crawl_url(source: str = None,
              prompt: str = None, 
              quick_option: AvailableQuickOption = None,
              model: str = None,
              api_key: str = None,
              response_schema: type[BaseModel] | None = None,
              llm_timeout: Optional[float] = 60,
              llm_retry: Optional[float] = 3,
              crawl_timeout: Optional[float] = 30, 
              crawl_retry: Optional[float] = 3
            ) -> CrawlUrlResponse:
    """
    Read a webpage and pull out specific information using an AI model.

    This function coordinates the whole process: it double-checks your inputs, 
    downloads the website text, selects the right instructions, and asks the AI 
    engine to format everything into your final organized answer.

    Args:
        source: The link to the website you want to read.
        prompt: Your own written instructions on what to look for.
        quick_option: A ready-made choice like summary, contacts, products, or auto.
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
        InvalidDataError: If any of your setting options or numbers are set incorrectly.
    """
    
    if source is None or str(source).strip() == "":
        raise UrlMissingError

    if (prompt is None or str(prompt).strip() == "" ) and (quick_option is None or str(quick_option).strip() == ""):
            raise PromptMissingError
    
    request_by_user: UrlExtractionRequest = None
    from graphcrawl_ai.utils.safe_cast import safe_cast
    try:
        request_by_user = UrlExtractionRequest(
            source = source,
            prompt = prompt,
            quick_option = quick_option,
            model = model,
            api_key = api_key,
            response_schema = response_schema,
            llm_timeout = safe_cast(llm_timeout, 'llm_timeout'),
            llm_retry = safe_cast(llm_retry, 'llm_retry'),
            crawl_timeout = safe_cast(crawl_timeout, 'crawl_timeout'),
            crawl_retry = safe_cast(crawl_retry, 'crawl_retry')
        )
    except ValidationError as e:
        err_msg = e.errors()
        failed_param = err_msg[0]["loc"][0]
        raise InvalidDataError(param_name=failed_param)
    
    request_to_llm = resolve_url_request(request=request_by_user)
    
    response_from_llm = llm_extract(request=request_to_llm)

    return response_from_llm