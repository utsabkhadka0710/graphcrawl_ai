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
    """Translate raw AI connection errors into clean internal system errors.

    This helper function looks at the root cause of an AI framework error and 
    converts it into a specific, easy-to-read app exception so the rest of the 
    system knows exactly what went wrong.

    Args:
        exception: The raw error thrown by the underlying Instructor or LiteLLM library.

    Returns:
        The matched custom exception class that fits the specific failure reason.
    """
    cause = exception.__cause__

    import litellm
    if isinstance(cause, (litellm.AuthenticationError,litellm.PermissionDeniedError)):
        return LLMAuthenticationError
    if isinstance(cause, litellm.Timeout):
        return LLMTimeoutError
    if isinstance(cause, litellm.RateLimitError):
        return LLMRateLimitError
    if isinstance(cause, litellm.ContextWindowExceededError):
        return LLMContextWindowExceededError
    if isinstance(exception, InstructorRetryException):
        return LLMRetryError
    if isinstance(cause, litellm.ServiceUnavailableError):
        return LLMUnavailabeError
    if isinstance(cause, (litellm.APIConnectionError, litellm.APIError)):
        return APIError
    return LLMUnknownError


def llm_extract(request:type[ExtractionJobToLLM]) -> type[BaseModel]:
    """Send instructions and webpage content to the chosen AI provider to extract clean data.

    This function sets up a universal client capable of talking to various AI providers. 
    It passes your prompt instructions and text content to the AI, manages response 
    deadlines and repeat attempts, and returns the information formatted precisely 
    to your requested data layout.

    Args:
        request: The pre-arranged data package containing the text content, 
            the prompt instructions, target model name, api keys, and retry configurations.

    Returns:
        An organized data object that matches the requested response template layout.

    Note:
        If the AI network request fails, runs out of time, or runs into access issues, 
        the function intercepts the problem and raises a clear, categorized internal error.
    """
    content = request.content
    prompt = request.prompt
    timeout = request.llm_timeout
    retry = request.llm_retry
    model = request.model
    api_key = request.api_key
    response_schema = request.response_schema

    client = CLIENT()

    try:
        response = client.sync_client().create(
            model=model,
            api_key = api_key,
            response_model=response_schema,
            timeout=timeout,
            num_retries=retry,
            max_retries=retry,
            messages=[
                {'role':'system','content':prompt},
                {'role':'user','content':content}
            ],
        )
    except InstructorError as e:
        raise _map_exceptions(exception=e)

    return response