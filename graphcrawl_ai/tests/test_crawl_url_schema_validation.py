import pytest
import httpx, respx
from unittest.mock import patch, AsyncMock
from graphcrawl_ai import crawl_url
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import ResponseSchemaMissingError


from pydantic import BaseModel
class MockResponseSchema(BaseModel):
    foo: str
    bar: str

@respx.mock
@pytest.mark.asyncio
async def test_valid_schema():
    with patch('graphcrawl_ai.crawler.crawl_url.llm_extract', new_callable=AsyncMock) as mock_extract:
        respx.get(url="https://graphcrawl.ai").mock(
            return_value=httpx.Response(
                status_code=200,
                    text="<p>GraphCrawlAI is an AI powered Python web scraper/crawler which is heavily under work rn."
                )
        )
        mock_extract.return_value = MockResponseSchema(
            foo = "mock foo response",
            bar = "mock bar response"
        )
        response = await crawl_url(
            source="https://graphcrawl.ai",
            prompt="Extract summary form this page",
            model="provider/model",
            api_key="A1B2C3D4E5",
            response_schema=MockResponseSchema
        )

        assert isinstance(response, MockResponseSchema)
        assert response.foo == "mock foo response"
        assert response.bar == "mock bar response"

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "schema",
    [
        "abc",
        123,
        12.3,
        [2,"summary"],
        ("summary",1),
        {"response":"summary"},
        {3, "summary"},
        None,
        True
    ],
    ids = ["string-as-schema", "int-as-schema", "float-as-schema",
           "list-as-schema","tuple-as-schema", "dict-as-schema",
           "set-as-schema", "none-as-schema", "bool-as-schema"]
)
async def test_invalid_schema(schema, respx_mock):
    respx_mock.get(url="https://graphcrawl.ai").mock(
        return_value=httpx.Response(
            status_code=200,
            text="<p>GraphCrawlAI is an AI powered Python web scraper/crawler which is heavily under work rn."
        )
    )
    with pytest.raises(ResponseSchemaMissingError):
        await crawl_url(
            source="https://graphcrawl.ai",
            prompt="Extract summary form this page",
            model="provider/model",
            api_key="A1B2C3D4E5",
            response_schema=schema
        )