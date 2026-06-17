from graphcrawl_ai.llm.request_resolver.user_url_request_resolver import resolve_url_request
from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest, AvailableQuickOption
from graphcrawl_ai.llm.gemini_extractor import get_response_gemini
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
              llm_timeout: Optional[float] = 60,
              llm_retry: Optional[float] = 3,
              crawl_timeout: Optional[float] = 30, 
              crawl_retry: Optional[float] = 3,
              response_schema: type[BaseModel] | None = None 
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
    
    timeout_and_retry_params = (llm_timeout, llm_retry, crawl_timeout, crawl_retry)
    if all(isinstance(param, str) and not param.isdigit() for param in timeout_and_retry_params):
         raise
    
    request_by_user: UrlExtractionRequest = None

    from graphcrawl_ai.utils.safe_cast import safe_cast
    try:
        request_by_user = UrlExtractionRequest(
            source = source,
            prompt = prompt,
            quick_option = quick_option,
            llm_timeout = safe_cast(llm_timeout, 'llm_timeout'),
            llm_retry = safe_cast(llm_retry, 'llm_retry'),
            crawl_timeout = safe_cast(crawl_timeout, 'crawl_timeout'),
            crawl_retry = safe_cast(crawl_retry, 'crawl_retry'),
            response_schema = response_schema
        )
    except ValidationError as e:
        err_msg = e.errors()
        failed_param = err_msg[0]["loc"][0]
        raise InvalidDataError(param_name=failed_param)
    
    request_to_llm, response_schema = resolve_url_request(request=request_by_user)
    
    response_from_llm = get_response_gemini(request=request_to_llm, response_schema=response_schema)

    return response_from_llm