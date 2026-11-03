import pytest
from pydantic import BaseModel, HttpUrl, ValidationError

from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest
from graphcrawl_ai.models.crawl_url.response_models.llm_response import UrlSummaryResponse
from graphcrawl_ai.llm.prompts import summary

class MockResponseSchema(BaseModel):
    foo: str
    bar: int

def test_valid_input():
    request = UrlExtractionRequest(
        source="https://foo.bar",
        prompt="Extract all the foo.",
        quick_option="summary",
        model="foo/bar",
        api_key="xxxx-xxxx-xxxx-xxxx",
        response_schema=MockResponseSchema,
        llm_timeout=60,
        llm_retry=4,
        crawl_timeout=60,
        crawl_retry=4
    )

    assert request.source == HttpUrl("https://foo.bar")
    assert request.prompt == "Extract all the foo."
    assert request.quick_option == "summary"
    assert request.model == "foo/bar"
    assert request.response_schema == MockResponseSchema
    assert request.llm_timeout == 60
    assert request.llm_retry == 4
    assert request.crawl_timeout == 60
    assert request.crawl_retry == 4


@pytest.mark.parametrize(
    "test_prompt, test_quick_option, test_response_schema, resolved_prompt, resolved_schema",
    [
        (None, "summary", None, summary, UrlSummaryResponse),
        (None, "summary", MockResponseSchema, summary, UrlSummaryResponse),
        ("mock prompt", None, MockResponseSchema, "mock prompt", MockResponseSchema),
        ("mock prompt", "summary", MockResponseSchema, "mock prompt", MockResponseSchema)
    ],
    ids=[
        "quick_option-only",
        "quick_option-and-response_schema",
        "prompt-and-response_schema",
        "prompt-quick_option-and-response_schema"
    ]
)
def test_resolve_valid_quick_option_and_prompt(
    test_prompt,
    test_quick_option,
    test_response_schema,
    resolved_prompt,
    resolved_schema
):
    request = UrlExtractionRequest(
        source="https://foo.bar",
        prompt=test_prompt,
        quick_option=test_quick_option,
        model="foo/bar",
        api_key="xxxx-xxxx-xxxx-xxxx",
        response_schema=test_response_schema,
    )

    assert request.prompt == resolved_prompt
    assert request.quick_option == test_quick_option
    assert request.response_schema == resolved_schema


@pytest.mark.parametrize(
    "test_prompt, test_quick_option, test_response_schema",
    [
        (1, None, MockResponseSchema),
        (None, 1, None),
        (None, "invalid", None),
        ("mock prompt", None, None),
        ("mock prompt", "summary", None),
        (None, None, None),
        (None, None, MockResponseSchema)
    ],
    ids=[
        "int-prompt",
        "int-quick_option",
        "invalid-quick_option",
        "prompt-without-response_schema",
        "prompt-quick_option-no-response_schema",
        "no-prompt-no-quick_option-no-response_schema",
        "no-prompt-no-quick_option-yes-response_schema"
    ]
) 
def test_resolve_invalid_quick_option_and_prompt(test_prompt, test_quick_option, test_response_schema):
    with pytest.raises(ValidationError):
        UrlExtractionRequest(
            source="https://foo.bar",
            prompt=test_prompt,
            quick_option=test_quick_option,
            model="foo/bar",
            api_key="xxxx-xxxx-xxxx-xxxx",
            response_schema=test_response_schema,
        )


@pytest.mark.parametrize(
    "malformed_url",
    [
        "example.com",
        "htt://example.com",
        "https:/example.com",
        "https:example.com",
        "http//example.com",
        "https://",
        "://example.com",
        "://",
        "https://example:foo",
        "https://foo:example.com",
        "https://example.com\n",
        "https://example.com\x1f",
        "https://[example].com",
    ]
)
def test_invalid_source(malformed_url):
    with pytest.raises(ValidationError):
        UrlExtractionRequest(
            source=malformed_url,
            quick_option="summary",
            model="foo/bar"
        )


@pytest.mark.parametrize(
    "invalid_model",
    [
        1,
        3.14,
        "  ",
        None,
        ['foo/bar']
    ],
    ids=[
        "int-as-model",
        "float-as-model",
        "whitespace-as-model",
        "none-as-model",
        "list-as-model"
    ]
)
def test_invalid_model(invalid_model):
    with pytest.raises(ValidationError):
        UrlExtractionRequest(
            source="https://foo.bar",
            prompt="Extract all the foo.",
            quick_option="summary",
            model=invalid_model,
            api_key="xxxx-xxxx-xxxx-xxxx",
            response_schema=MockResponseSchema,
            llm_timeout=60,
            llm_retry=4,
            crawl_timeout=60,
            crawl_retry=4
        )

