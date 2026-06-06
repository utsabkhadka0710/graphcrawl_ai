from graphcrawl_ai.llm.promt_resolver.url_prompt_resolver import resolve_prompt
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_user import UrlExtractionRequestByUser
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_internal import ExtractionRequestToLLM
from graphcrawl_ai.llm.gemini_extractor import get_response_gemini
from typing import Literal

# =====================================================================================================
#             Method to crawl/scrape from URL with custom prompt or given quick options
# =====================================================================================================
def crawl_url(source: str, prompt: str = None, quick_option: Literal["summary","contacts","products","auto"] = None) -> ExtractionRequestToLLM:
    """ Extracts the structured data from URL using LLM-based resolver

    This function u
    """
    request_by_user = UrlExtractionRequestByUser(
        source = source,
        prompt = prompt,
        quick_option = quick_option
    )


    request_to_llm = resolve_prompt(request=request_by_user)
    response_from_llm = get_response_gemini(request=request_to_llm)

    if (not prompt) and (not quick_option):
        class InvalidRequest(Exception): pass
        raise InvalidRequest("Prompt missing, request() must have either a prompt or an quick option. You request looks like: request(source='...') it should be like request(source='...',prompt='...') or request(source='...',quick_option='...')")

    
    return response_from_llm