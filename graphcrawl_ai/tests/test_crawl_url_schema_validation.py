import pytest
import httpx, respx

from graphcrawl_ai import crawl_url
from graphcrawl_ai.exceptions.crawler.crawl_url_exceptions import ResponseSchemaMissingError


from pydantic import BaseModel
class Schema(BaseModel):
    title: str
    summary: str

@respx.mock
def test_valid_schema():
    respx.get(url="https://graphcrawl.ai").mock(
        return_value=httpx.Response(
            status_code=200,
                text="<p>GraphCrawlAI is an AI powered Python web scraper/crawler which is heavily under work rn."
            )
    )
    try:
        crawl_url(
            source="https://graphcrawl.ai",
            prompt="Extract summary form this page",
            model="provider/model",
            api_key="A1B2C3D4E5",
            response_schema=Schema
        )
    except ResponseSchemaMissingError:
        pytest.fail("schema validation custom exception raised test failed!")
    except Exception:
        pass

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
def test_invalid_schema(schema, respx_mock):
    respx_mock.get(url="https://graphcrawl.ai").mock(
        return_value=httpx.Response(
            status_code=200,
            text="<p>GraphCrawlAI is an AI powered Python web scraper/crawler which is heavily under work rn."
        )
    )
    try:
        crawl_url(
            source="https://graphcrawl.ai",
            prompt="Extract summary form this page",
            model="provider/model",
            api_key="A1B2C3D4E5",
            response_schema=schema
        )
    except ResponseSchemaMissingError:
        pass
    except Exception:
        pytest.fail("schema validation custom exception didn't raised test failed!")