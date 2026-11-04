from graphcrawl_ai.llm import prompts
from graphcrawl_ai.extraction.html_from_url import fetch_html
from graphcrawl_ai.extraction.text_from_html import extract_content_from_html
from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest
from graphcrawl_ai.models.crawl_url.request_models.request_to_llm import ExtractionJobToLLM


async def resolve_url_request(request: UrlExtractionRequest) -> ExtractionJobToLLM:
    """Download website text and bundle it with the correct AI instructions and settings.

    This function coordinates preparing a web-reading task for the AI. It downloads 
    the webpage content, extracts the useful text, and determines the correct target 
    instructions and structural template to use based on user options or a custom format.

    Args:
        request: The initial settings from the user, including the website link, 
            the chosen AI model, and data extraction instructions.

    Returns:
        The fully prepared data package containing the webpage text, chosen model, 
        and validation template, ready to be sent directly to the AI engine.
    """
    
    source = str(request.source) #This is type casted to str because 'source' is stored initally as 'pydantic.HttpUrl' but in 'fetch_html' httpx expects 'str' or 'httpx.URL'
    prompt = request.prompt
    quick_option = request.quick_option
    model = request.model
    response_schema = request.response_schema
    api_key = request.api_key
    llm_timeout = request.llm_timeout
    llm_retry = request.llm_retry
    crawl_timeout = request.crawl_timeout
    crawl_retry = request.crawl_retry

    
    raw_html = await fetch_html(url=source,crawl_timeout=crawl_timeout, crawl_retry=crawl_retry)
    clean_content = extract_content_from_html(html_content=raw_html)
    

    request_to_llm = ExtractionJobToLLM(
        content=clean_content,
        prompt=prompt,
        model=model,
        api_key=api_key,
        response_schema=response_schema,
        llm_timeout=llm_timeout,
        llm_retry=llm_retry
    )

    return request_to_llm