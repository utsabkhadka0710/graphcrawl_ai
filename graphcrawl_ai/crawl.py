from graphcrawl_ai.llm.promt_resolver.url_prompt_resolver import resolve_prompt
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_user import UrlExtractionRequestByUser
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_internal import ExtractionRequestToLLM
from graphcrawl_ai.llm.gemini_extractor import get_response_gemini
from typing import Literal, Optional


def crawl_url(source: str, prompt: str = None, quick_option: Literal["summary","contacts","products","auto"] = None, timeout:Optional[float]=30, retry:Optional[int]=3) -> ExtractionRequestToLLM:
    """Extract and structure data from a target URL using an LLM-based extraction engine.

    This function orchestrates the end-to-end extraction lifecycle. It takes the user's
    raw input parameters, runs schema validation via the user request model, dispatches the 
    configuration to the prompt resolver to standardize the LLM instruction set, and finally 
    invokes the LLM handler to execute the web scrape operation.

    Args:
        source: The target website URL string to be crawled and processed.
        prompt: An optional custom natural language text block directing the LLM's parsing behavior.
        quick_option: An optional shortcut token representing a pre-configured, common extraction use case.
        timeout: Total continuous duration in seconds allowed for fetching and processing operations.
        retry: Total attempt threshold allowed for establishing connectivity before abandoning the pipeline.

    Returns:
        An ExtractionRequestToLLM object holding the final parsed web content 
        and resolved text instructions.

    Raises:
        InvalidRequest: If both `prompt` and `quick_option` are omitted from the call signature, 
            rendering the extraction intent unresolvable.
    """
    request_by_user = UrlExtractionRequestByUser(
        source = source,
        prompt = prompt,
        quick_option = quick_option,
        timeout = timeout,
        retry = retry
    )


    request_to_llm = resolve_prompt(request=request_by_user)
    response_from_llm = get_response_gemini(request=request_to_llm)

    if (not prompt) and (not quick_option):
        class InvalidRequest(Exception): pass
        raise InvalidRequest("Prompt missing, request() must have either a prompt or an quick option. You request looks like: request(source='...') it should be like request(source='...',prompt='...') or request(source='...',quick_option='...')")

    
    return response_from_llm