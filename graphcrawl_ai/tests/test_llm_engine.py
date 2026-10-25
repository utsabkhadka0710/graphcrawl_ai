import pytest
import litellm
import httpx
from pydantic import BaseModel
from unittest.mock import AsyncMock, patch

from graphcrawl_ai.llm.engine import llm_extract, _map_exceptions
from graphcrawl_ai.models.crawl_url.request_models.request_to_llm import ExtractionJobToLLM

from instructor.core import InstructorError, InstructorRetryException
from graphcrawl_ai.exceptions.llm.llm_extractor_exceptions import (
    LLMAuthenticationError,
    LLMNotFoundError,
    LLMRetryError,
    LLMTimeoutError,
    LLMRateLimitError,
    LLMUnavailableError,
    LLMContextWindowExceededError,
    APIError,
    LLMUnknownError
)


class LLMEngineMockResponseModel(BaseModel):
    """Dummy Pydantic schema used to mock structured outputs from the LLM engine."""
    summary: str
    information: list[str]

@pytest.mark.asyncio
async def test_llm_extract_valid_request_forward_and_return_response():
    mock_request = ExtractionJobToLLM(
        content="This is an test parsed content cleaned from fetched HTML",
        prompt="Extract useful information",
        model="provider/model",
        api_key="model-api-key",
        response_schema=LLMEngineMockResponseModel,
        llm_timeout=30,
        llm_retry=2
    )
    with patch('graphcrawl_ai.llm.engine.Client') as MockClientClass:
        mock_client_instance = MockClientClass.return_value

        mock_create = AsyncMock()
        mock_client_instance.get_client.return_value.create = mock_create

        mock_llm_response = LLMEngineMockResponseModel(
            summary="This is an mock summary returned by mock LLM",
            information=[
                "This is mock informantion 1",
                "This is mock informantion 2",
                "This is mock informantion 3",
            ]
        )

        mock_create.return_value = mock_llm_response

        result = await llm_extract(request=mock_request)

        assert result == mock_llm_response

        mock_create.assert_awaited_once_with(
            model='provider/model',
            api_key='model-api-key',
            response_model=LLMEngineMockResponseModel,
            timeout=30,
            num_retries=2,
            max_retries=2,
            messages=[
                {'role': 'system', 'content': 'Extract useful information'},
                {'role': 'user', 'content': 'This is an test parsed content cleaned from fetched HTML'}
            ]
        )


def wrap_instructor_error_cause(cause: Exception) -> InstructorError:
    """Wrap an underlying provider exception inside an InstructorError instance to mimic real runtime wrapper behavior."""
    outer_exc = InstructorError()
    outer_exc.__cause__ = cause
    return outer_exc


def lite_exception(cls, **kw) -> Exception:
    """Helper factory that builds pre-configured LiteLLM exception instances for testing."""
    return cls(
        message="error",
        llm_provider="mock-provider",
        model="mock-model",
        **kw
    )


def fake_response() -> httpx.Response:
    """Construct a mock HTTP 403 response object for permission testing."""
    return httpx.Response(
        status_code=403,
        request=httpx.Request(method="POST", url="https://mock.com")
    )


@pytest.mark.parametrize(
    "raw_exception, raised_exception",
    [
        # LiteLLM's errors
        (lite_exception(litellm.AuthenticationError), LLMAuthenticationError),
        (lite_exception(litellm.PermissionDeniedError, response=fake_response()), LLMAuthenticationError),
        (lite_exception(litellm.NotFoundError), LLMNotFoundError),
        (lite_exception(litellm.Timeout), LLMTimeoutError),
        (lite_exception(litellm.RateLimitError), LLMRateLimitError),
        (lite_exception(litellm.ServiceUnavailableError), LLMUnavailableError),
        (lite_exception(litellm.ContextWindowExceededError), LLMContextWindowExceededError),
        (lite_exception(litellm.APIConnectionError), APIError),
        (lite_exception(litellm.APIError, status_code=500), APIError)
    ],
    ids=[
        "authentication-error",
        "permission-denied-authentication-error",
        "llm-not-found-error",
        "timeout-error",
        "rate-limit-error",
        "service-unavailable-error",
        "context-window-exceeded-error",
        "api-connection-error",
        "api-error"
    ]
)
def test_llm_engine_map_litellm_exceptions(raw_exception, raised_exception):
    """Verify that LiteLLM provider exceptions wrapped inside Instructor errors map to their correct domain exceptions."""
    assert _map_exceptions(wrap_instructor_error_cause(raw_exception)) is raised_exception


@pytest.mark.parametrize(
    "raw_exception, raised_exception",
    [
        # Instructor's error
        (InstructorRetryException(n_attempts=3, total_usage=3), LLMRetryError),

        # Unexpected error
        (InstructorError(), LLMUnknownError),
        (TypeError(), LLMUnknownError)
    ],
    ids=[
        "retry-error",
        "unknown-error-from-instructor-error",
        "unknown-error-from-non-instructor-error"
    ]
)
def test_llm_engine_map_non_litellm_exceptions(raw_exception, raised_exception):
    """Verify that Instructor retry failures and unexpected fallback errors map to domain exception types."""
    assert _map_exceptions(raw_exception) is raised_exception



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raw_exception, raised_exception",
    [
        # LiteLLM's errors
        (lite_exception(litellm.AuthenticationError), LLMAuthenticationError),
        (lite_exception(litellm.PermissionDeniedError, response=fake_response()), LLMAuthenticationError),
        (lite_exception(litellm.NotFoundError), LLMNotFoundError),
        (lite_exception(litellm.Timeout), LLMTimeoutError),
        (lite_exception(litellm.RateLimitError), LLMRateLimitError),
        (lite_exception(litellm.ServiceUnavailableError), LLMUnavailableError),
        (lite_exception(litellm.ContextWindowExceededError), LLMContextWindowExceededError),
        (lite_exception(litellm.APIConnectionError), APIError),
    ],
    ids=[
        "extract-authentication-error",
        "extract-permission-denied-authentication-error",
        "llm-not-found-error",
        "extract-timeout-error",
        "extract-rate-limit-error",
        "extract-service-unavailable-error",
        "extract-context-window-exceeded-error",
        "extract-api-connection-error"
    ]
)
async def test_llm_extract_exeption_mapping(raw_exception, raised_exception):
    mock_request = ExtractionJobToLLM(
        content="This is an test parsed content cleaned from fetched HTML",
        prompt="Extract useful information",
        model="provider/model",
        api_key="model-api-key",
        response_schema=LLMEngineMockResponseModel
    )
    with patch('graphcrawl_ai.llm.engine.Client') as MockClientClass:
        mock_client_instance = MockClientClass.return_value

        mock_create = AsyncMock()
        mock_client_instance.get_client.return_value.create = mock_create

        mock_create.side_effect = wrap_instructor_error_cause(raw_exception)

        with pytest.raises(raised_exception):
            await llm_extract(request=mock_request)