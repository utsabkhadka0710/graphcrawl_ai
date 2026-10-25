import pytest
import litellm
import httpx
from pydantic import BaseModel
from unittest.mock import AsyncMock, patch

from graphcrawl_ai.llm.engine import llm_extract, _map_exceptions
from graphcrawl_ai.models.crawl_url.request_models.request_to_llm import ExtractionJobToLLM
from graphcrawl_ai.llm.prompts import EXTRACTION_SYSTEM_PROMPT

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
    """Define a mock Pydantic schema for the structured response returned by the LLM."""
    summary: str
    information: list[str]


@pytest.mark.asyncio
async def test_llm_extract_valid_request_forward_and_return_response():
    """Verify that a valid extraction request is forwarded correctly and its response is returned."""
    mock_request = ExtractionJobToLLM(
        content="This is an test parsed content cleaned from fetched HTML",
        prompt="Extract useful information",
        model="provider/model",
        api_key="model-api-key",
        response_schema=LLMEngineMockResponseModel,
        llm_timeout=30,
        llm_retry=2
    )

    # Mock the Client dependency to avoid making real LLM API calls.
    with patch('graphcrawl_ai.llm.engine.Client') as MockClientClass:
        mock_client_instance = MockClientClass.return_value

        # Use AsyncMock because create() is awaited by llm_extract().
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

        # Ensure the extraction result is returned unchanged.
        assert result == mock_llm_response

        # Verify that all request parameters are forwarded to the LLM client.
        mock_create.assert_awaited_once_with(
            model='provider/model',
            api_key='model-api-key',
            response_model=LLMEngineMockResponseModel,
            timeout=30,
            num_retries=2,
            max_retries=2,
            messages=[
                {
                    "role": "system",
                    "content": EXTRACTION_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": (
                        f"Extraction Task: \nExtract useful information\n\n"
                        f"Source Cotent: \nThis is an test parsed content cleaned from fetched HTML"
                    )
                }
            ]
        )


def wrap_instructor_error_cause(cause: Exception) -> InstructorError:
    """Create an InstructorError whose __cause__ references the supplied provider exception."""
    outer_exc = InstructorError()
    outer_exc.__cause__ = cause
    return outer_exc


def lite_exception(cls, **kw) -> Exception:
    """Create a LiteLLM exception with the required provider and model metadata for testing."""
    return cls(
        message="error",
        llm_provider="mock-provider",
        model="mock-model",
        **kw
    )


def fake_response() -> httpx.Response:
    """Create a mock HTTP 403 response for constructing permission-denied exceptions."""
    return httpx.Response(
        status_code=403,
        request=httpx.Request(method="POST", url="https://mock.com")
    )


@pytest.mark.parametrize(
    "raw_exception, raised_exception",
    [
        # Verify mappings for specific LiteLLM provider errors.
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
    """Verify that wrapped LiteLLM exceptions map to their corresponding domain exception classes."""
    # Simulate an Instructor error carrying the original provider exception as its cause.
    instructor_error = wrap_instructor_error_cause(raw_exception)

    assert _map_exceptions(instructor_error) is raised_exception


@pytest.mark.parametrize(
    "raw_exception, raised_exception",
    [
        # Instructor retry exhaustion should map to the dedicated retry error.
        (InstructorRetryException(n_attempts=3, total_usage=3), LLMRetryError),

        # Unrecognized errors should use the fallback domain exception.
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
    """Verify retry-error mapping and fallback behavior for unrecognized exception types."""
    assert _map_exceptions(raw_exception) is raised_exception


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raw_exception, raised_exception, should_wrap",
    [
        # Provider exceptions are wrapped to simulate the cause structure handled by the engine.
        (lite_exception(litellm.AuthenticationError), LLMAuthenticationError, True),
        (lite_exception(litellm.PermissionDeniedError, response=fake_response()), LLMAuthenticationError, True),
        (lite_exception(litellm.NotFoundError), LLMNotFoundError, True),
        (lite_exception(litellm.Timeout), LLMTimeoutError, True),
        (lite_exception(litellm.RateLimitError), LLMRateLimitError, True),
        (lite_exception(litellm.ServiceUnavailableError), LLMUnavailableError, True),
        (lite_exception(litellm.ContextWindowExceededError), LLMContextWindowExceededError, True),
        (lite_exception(litellm.APIConnectionError), APIError, True),
        (lite_exception(litellm.APIError, status_code=500), APIError, True),

        # Instructor exceptions are raised directly to test the engine's exception handler.
        (InstructorRetryException(n_attempts=3, total_usage=3), LLMRetryError, False),
        (InstructorError(), LLMUnknownError, False),

        # A non-Instructor exception should propagate unchanged through llm_extract().
        (TypeError(), TypeError, False)
    ],
    ids=[
        "extract-authentication-error",
        "extract-permission-denied-authentication-error",
        "extract-llm-not-found-error",
        "extract-timeout-error",
        "extract-rate-limit-error",
        "extract-service-unavailable-error",
        "extract-context-window-exceeded-error",
        "extract-api-connection-error",
        "extract-api-error",
        "extract-retry-error",
        "extract-unknown-error-from-instructor-error",
        "extract-non-instructor-error"
    ]
)
async def test_llm_extract_exception_mapping(raw_exception, raised_exception, should_wrap):
    """Verify exception translation during extraction and propagation of non-Instructor errors."""
    mock_request = ExtractionJobToLLM(
        content="This is an test parsed content cleaned from fetched HTML",
        prompt="Extract useful information",
        model="provider/model",
        api_key="model-api-key",
        response_schema=LLMEngineMockResponseModel
    )

    # Replace the client so the test exercises error handling without external API calls.
    with patch('graphcrawl_ai.llm.engine.Client') as MockClientClass:
        mock_client_instance = MockClientClass.return_value

        mock_create = AsyncMock()
        mock_client_instance.get_client.return_value.create = mock_create

        # Choose the exception structure explicitly for the scenario being tested.
        if should_wrap:
            mock_create.side_effect = wrap_instructor_error_cause(raw_exception)
        else:
            mock_create.side_effect = raw_exception

        # Verify that llm_extract() raises the expected domain exception,
        # or propagates the original exception when it is not handled.
        with pytest.raises(raised_exception):
            await llm_extract(request=mock_request)