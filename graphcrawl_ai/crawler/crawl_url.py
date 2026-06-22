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
    Scrapes a webpage and extracts structured data using an AI model.

    This function handles the end-to-end process: validating user input, 
    preparing the request, and querying the Gemini AI to extract information 
    based on the provided prompt or quick option.

    Args:
        source (str): The URL of the website to scrape.
        prompt (str, optional): Custom instructions for the AI on what to extract.
        quick_option (AvailableQuickOption, optional): A predefined extraction mode 
            (e.g., 'summary', 'contacts').
        llm_timeout (float, optional): Maximum time (seconds) to wait for AI response.
        llm_retry (float, optional): Number of times to retry the AI request on failure.
        crawl_timeout (float, optional): Maximum time (seconds) to wait for page load.
        crawl_retry (float, optional): Number of times to retry the page load on failure.
        response_schema (type[BaseModel], optional): A Pydantic model to enforce the 
            structure of the AI output.

    Returns:
        CrawlUrlResponse: The extracted data structured according to the provided schema.

    Raises:
        UrlMissingError: If the 'source' argument is missing or an empty string.
        PromptMissingError: If neither a 'prompt' nor a 'quick_option' is provided.
        InvalidDataError: If any of the provided parameters fail validation checks.
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