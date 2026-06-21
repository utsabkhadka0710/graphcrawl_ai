from pydantic import BaseModel
from graphcrawl_ai.llm.client import CLIENT
from graphcrawl_ai.llm.config import build_kwargs
from graphcrawl_ai.models.crawl_url.request_models.request_to_llm import ExtractionJobToLLM
from instructor.core import (
    InstructorError,
    InstructorRetryException
)
from graphcrawl_ai.exceptions.llm.llm_extractor_exceptions import(
    LLMAuthenticationError,
    LLMRetryError,
    LLMTimeoutError,
    LLMRateLimitError,
    LLMUnavailabeError,
    LLMContextWindowExceededError,
    APIError,
    LLMUnknownError
)

def _map_exceptions(exception: InstructorError):
    cause = exception.__cause__

    import litellm
    if isinstance(cause, (litellm.AuthenticationError,litellm.PermissionDeniedError)):
        return LLMAuthenticationError
    if isinstance(exception, InstructorRetryException):
        return LLMRetryError
    if isinstance(cause, litellm.Timeout):
        return LLMTimeoutError
    if isinstance(cause, litellm.RateLimitError):
        return LLMRateLimitError
    if isinstance(cause, litellm.ContextWindowExceededError):
        return LLMContextWindowExceededError
    if isinstance(cause, litellm.ServiceUnavailableError):
        return LLMUnavailabeError
    if isinstance(cause, (litellm.APIConnectionError, litellm.APIError)):
        return APIError
    return LLMUnknownError


def llm_extract(request:type[ExtractionJobToLLM]) -> type[BaseModel]:
    content = request.content
    prompt = request.prompt
    timeout = request.llm_timeout
    retry = request.llm_retry
    response_schema = request.response_schema

    client = CLIENT()

    try:
        response = client.sync_client().create(
            messages=[
                {'role':'system','content':prompt},
                {'role':'user','content':content}
            ],
            model='gemini/gemini-3.1-flash-lite',
            response_model=response_schema,
            timeout=timeout,
            max_retries=retry
        )
    except InstructorError as e:
        raise _map_exceptions(exception=e)

    return response