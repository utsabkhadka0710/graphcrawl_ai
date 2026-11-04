import pytest
from pydantic import BaseModel, HttpUrl, ValidationError

from graphcrawl_ai.models.crawl_url.request_models.user_request import UrlExtractionRequest
from graphcrawl_ai.models.crawl_url.response_models.llm_response import UrlSummaryResponse
from graphcrawl_ai.llm.prompts import summary
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import(
    UrlMissingError,
    PromptMissingError,
    ResponseSchemaMissingError
)

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
    "test_prompt, test_quick_option, test_response_schema, raised_exception",
    [
        (1, None, MockResponseSchema, ValidationError),
        (None, 1, None, ValidationError),
        (None, "invalid", None, ValidationError),
        ("mock prompt", None, None, ResponseSchemaMissingError),
        ("mock prompt", "summary", None, ResponseSchemaMissingError),
        (None, None, None, PromptMissingError),
        (None, None, MockResponseSchema, PromptMissingError),
        ("  ", None, MockResponseSchema, PromptMissingError),
        ("", None, MockResponseSchema, PromptMissingError)
    ],
    ids=[
        "int-prompt",
        "int-quick_option",
        "invalid-quick_option",
        "prompt-without-response_schema",
        "prompt-quick_option-no-response_schema",
        "no-prompt-no-quick_option-no-response_schema",
        "no-prompt-no-quick_option-yes-response_schema",
        "whitespace-only-prompt-no-quick_option-yes-response_schema",
        "none-string-prompt-"
    ]
) 
def test_resolve_invalid_quick_option_and_prompt(
    test_prompt,
    test_quick_option,
    test_response_schema,
    raised_exception
):
    with pytest.raises(raised_exception):
        UrlExtractionRequest(
            source="https://foo.bar",
            prompt=test_prompt,
            quick_option=test_quick_option,
            model="foo/bar",
            api_key="xxxx-xxxx-xxxx-xxxx",
            response_schema=test_response_schema,
        )


@pytest.mark.parametrize(
    "url, raised_exception",
    [
        ("", UrlMissingError),
        ("  ", UrlMissingError),
        (None, UrlMissingError),
        (["https://foo.bar"], ValidationError)
    ],
    ids=[
        "empty-string-as-source",
        "white-space-as-source",
        "none-as-source",
        "list-as-source"
    ]
)
def test_invalid_source(url, raised_exception):
    with pytest.raises(raised_exception):
        UrlExtractionRequest(
            source=url,
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


def make_extraction_model_for_timeout_and_retry(
    crawl_timeout,
    crawl_retry,
    llm_timeout,
    llm_retry
):
    return UrlExtractionRequest(
        source="https://foo.bar",
        prompt="Extract all the foo.",
        quick_option="summary",
        model="foo/bar",
        api_key="xxxx-xxxx-xxxx-xxxx",
        response_schema=MockResponseSchema,
        llm_timeout=llm_timeout,
        llm_retry=llm_retry,
        crawl_timeout=crawl_timeout,
        crawl_retry=crawl_retry
    )

@pytest.mark.parametrize(
    "test_crawl_timeout, test_crawl_retry, test_llm_timeout, test_llm_retry",
    [
        (0, 4, 60, 4),
        (-1, 4, 60, 4),
        (60, -1, 60, 4),
        (60, 4, 0, 4),
        (60, 4, -1, 4),
        (60, 4, 60, -1),
        ('g', 4, 60, 4),
        (60, 'g', 60, 4),
        (60, 4, 'g', 4),
        (60, 4, 60, 'g'),
        ([60], 4, 60, 4),
        (60, [4], 60, 4),
        (60, 4, [60], 4),
        (60, 4, 60, [4])
    ],
    ids=[
        "zero-crawl-timeout",
        "negative-crawl-timeout",
        "negative-crawl-retry",
        "zero-llm-timeout",
        "negative-llm-timeout",
        "negative-llm-retry",
        "string-as-crawl-timeout",
        "string-as-crawl-retry",
        "string-as-llm-timeout",
        "string-as-llm-retry",
        "list-as-crawl-timeout",
        "list-as-crawl-retry",
        "list-as-llm-timeout",
        "list-as-llm-retry",
    ]
)
def test_invalid_crawl_timeout(
    test_crawl_timeout,
    test_crawl_retry,
    test_llm_timeout,
    test_llm_retry
):
    with pytest.raises(ValidationError):
        make_extraction_model_for_timeout_and_retry(
            crawl_timeout=test_crawl_timeout,
            crawl_retry=test_crawl_retry,
            llm_timeout=test_llm_timeout,
            llm_retry=test_llm_retry
        )