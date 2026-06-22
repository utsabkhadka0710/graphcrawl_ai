from pydantic import BaseModel
from graphcrawl_ai.llm import prompts
from graphcrawl_ai.extraction.html_from_url import fetch_html
from graphcrawl_ai.extraction.text_from_html import extract_content_from_html
from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest, QuickOption
from graphcrawl_ai.models.crawl_url.request_models.request_to_llm import ExtractionJobToLLM
from graphcrawl_ai.models.crawl_url.response_models.llm_response import (
    UrlPromptResponse,
    UrlSummaryResponse,
    UrlContactsResponse,
    UrlProductsResponse,
    UrlAutoResponse
)

def resolve_url_request(request: UrlExtractionRequest) -> ExtractionJobToLLM:
    """Download website text and match it with the correct AI instructions and template.

    This function handles the heavy lifting of loading the webpage, cleaning up 
    the text, and choosing the right instructions and data layout template. It uses 
    either the ready-made settings chosen by the user or switches to a custom setup 
    if the user provided their own template layout.

    Args:
        request: The initial settings from the user, including the website link 
            and options for what information to find.

    Returns:
        A pair containing two items:
        1. The prepared request object ready for the AI engine.
        2. The data layout template class used to check the final answer.

    Note:
        This function will stop and raise a ValueError if you forget to provide 
        either a custom prompt or a ready-made quick option.
    """
    
    source = request.source
    prompt = request.prompt
    quick_option = request.quick_option
    model = request.model
    api_key = request.api_key
    llm_timeout = request.llm_timeout
    llm_retry = request.llm_retry
    crawl_timeout = request.crawl_timeout
    crawl_retry = request.crawl_retry
    response_schema = UrlPromptResponse

    if quick_option and not prompt:
        match quick_option:
            case QuickOption.SUMMARY:
                prompt = prompts.summary
                response_schema = UrlSummaryResponse

            case QuickOption.CONTACTS:
                prompt = prompts.contacts
                response_schema = UrlContactsResponse

            case QuickOption.PRODUCTS:
                prompt = prompts.products
                response_schema = UrlProductsResponse

            case QuickOption.AUTO:
                prompt = prompts.auto
                response_schema = UrlAutoResponse

    raw_html = fetch_html(url=source,crawl_timeout=crawl_timeout, crawl_retry=crawl_retry)
    clean_content = extract_content_from_html(html_content=raw_html).content
    
    if request.response_schema is not None:
        response_schema = request.response_schema

    request_to_llm = ExtractionJobToLLM(
        content = clean_content,
        prompt = prompt,
        model = model,
        api_key = api_key,
        response_schema = response_schema,
        llm_timeout = llm_timeout,
        llm_retry = llm_retry
    )

    return request_to_llm