from graphcrawl_ai.llm.promt_resolver.url_prompt_resolver import resolve_prompt
from graphcrawl_ai.models.request import ExtractionRequestByUser, ExtractionRequestToLLM
from graphcrawl_ai.llm.gemini_extractor import get_response_gemini
from typing import Literal


def crawl_url(source: str, prompt: str = None, quick_option: Literal["summary","contacts","products","auto"] = None) -> ExtractionRequestToLLM:

    request_by_user = ExtractionRequestByUser(
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