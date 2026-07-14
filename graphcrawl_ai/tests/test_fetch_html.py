import asyncio
import pytest
import pytest_asyncio
import respx, httpx

from graphcrawl_ai.extraction.html_from_url import fetch_html
from graphcrawl_ai.exceptions.extration.html_from_url_exceptions import (
    InvalidUrl,
    HTTPStatusError,
    ProtocolError,
    NetworkError,
    RetryTimeoutError,

)

valid_base_url = "https://example-url.site/"

@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code",
    [200, 203, 206,],
    ids = ["status-code-200-OK", "status-code-203-Non-Authoritative Information", "status-code-206-Partial Content"]
)
async def test_fetch_html_return_html(status_code):
    """Confirm that the function returns raw HTML when the server answers with a successful status code."""
    my_route = respx.get(url=valid_base_url).mock(
        return_value=httpx.Response(status_code=status_code, text="<p>Mock success HTML.</p>")
    )  
    response = await fetch_html(url=valid_base_url)
    assert my_route.called
    assert my_route.call_count == 1
    assert response == "<p>Mock success HTML.</p>"


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code",
    [400, 401, 403, 404, 408,429,],
    ids = ["status-code-400-Bad Request", "status-code-401-Unauthorized", "status-code-403-Forbidden",
           "status-code-404-Not Found", "status-code-408-Request Timeout", "status-code-429- Too Many Requests"]
)
async def test_fetch_html_non_retriable_client_errors(status_code):
    """Confirm that standard client errors (4xx codes) fail immediately without triggering retries."""
    my_route = respx.get(url=valid_base_url).mock(return_value=httpx.Response(status_code=status_code))
    with pytest.raises(HTTPStatusError):
        await fetch_html(url=valid_base_url)
    assert my_route.called
    assert my_route.call_count == 1

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code",
    [500, 502, 503, 504, 505],
    ids = [
           "status-code-500-Internal Server Error",
           "status-code-502-Bad Gateway",
           "status-code-503-Service Unavailable",
           "status-code-504-Gateway Timeout",
           "status-code-505-HTTP Version Not Supported",
        ]
)
class TestFetchHtmlRetriableServerErrors:
    """Verify how the system handles temporary 5xx server issues using retries."""
    async def test_fails_all_three_retries(self, status_code, respx_mock):
        """Confirm that if the server remains broken through all attempts, a status error is raised."""
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[httpx.Response(status_code)]*3
        )
        with pytest.raises(HTTPStatusError):
            await fetch_html(url=valid_base_url, crawl_retry=3)
        assert my_route.call_count == 3
    async def test_fails_twice_succeeds_last_retry(self, status_code, respx_mock):
        """Confirm that recovery is successful if the server goes back up on the final retry attempt."""
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.Response(status_code), httpx.Response(status_code),
                httpx.Response(status_code=200, text="<p>Mock retry success on third attempt HTML.</p>")
            ]
        )
        response = await fetch_html(url=valid_base_url, crawl_retry=3)
        assert response == "<p>Mock retry success on third attempt HTML.</p>"
        assert my_route.call_count == 3
    async def test_fails_once_succeeds_on_second_attempt(self, status_code, respx_mock):
        """Confirm that recovery is successful if the server stops throwing errors on the second try."""
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.Response(status_code),
                httpx.Response(status_code=200, text="<p>Mock retry success on second attempt HTML.</p>")
            ]
        )
        response = await fetch_html(url=valid_base_url, crawl_retry=3)
        assert response == "<p>Mock retry success on second attempt HTML.</p>"
        assert my_route.call_count == 2

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "malformed_or_protocol_missing_url",
    [
        "example.com",
        "htt://example.com",
        "https:/example.com",
        "https:example.com",
        "http//example.com",
        "https://",
        "://example.com",
        "://"
    ],
    ids = ["protocol-missing",
           "invalid-protocol-schema",
           "missing-one-slash-in-protocol-hierarchy-separator",
           "missing-protocol-hierarchy-separator",
           "invalid-protocol-url",
           "missing-host",
           "missing-schema",
           "missing-schema-and-host"]
)
async def test_fetch_html_protocol_error(malformed_or_protocol_missing_url):
    """Confirm that URLs missing standard 'http://' or 'https://' components trigger a ProtocolError."""
    with pytest.raises(ProtocolError):
        await fetch_html(url=malformed_or_protocol_missing_url)

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "malformed_or_invalid_url",
    [
        "https://example:foo",
        "https://foo:example.com",
        "https://example.com\n",
        "https://example.com\x1f",
        "https://😭example.com",
        "https://[example].com",
    ],
    ids = ["non-numeric-port", "url-at-host", "escape-sequence-in-url", "ascii-control-character-in-url",
           "unencoded-emoji-in-url", "invalid-character-in-url"]
)
async def test_fetch_html_malformed_or_invalid_url(malformed_or_invalid_url):
    """Confirm that totally broken, typo-ridden, or illegal URLs correctly trigger an InvalidUrl error."""
    with pytest.raises(InvalidUrl):
        await fetch_html(url=malformed_or_invalid_url)

@respx.mock
@pytest.mark.asyncio
async def test_fetch_html_network_error():
    """Confirm that infrastructure or physical connectivity errors get converted to an internal NetworkError."""
    my_route = respx.get(url=valid_base_url).mock(side_effect=httpx.NetworkError(message="Mock NetworkError"))
    with pytest.raises(NetworkError):
        await fetch_html(url=valid_base_url)
    assert  my_route.called
    assert my_route.call_count == 1

@pytest.mark.asyncio
class TestFetchHtmlTimeout:
    """Verify how the system reacts when request connections slow down and hit timeouts."""
    async def test_timeouts_all_three_retries(self, respx_mock):
        """Confirm that if the network times out continuously, a RetryTimeoutError is thrown."""
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[httpx.TimeoutException]*3
        )
        with pytest.raises(RetryTimeoutError):
            await fetch_html(url=valid_base_url, crawl_timeout=5)
        assert my_route.call_count == 3
    async def test_timeouts_twice_succeeds_on_last_attempt(self, respx_mock):
        """Confirm that if the network speeds up right after one timeout, it successfully finishes on the second try."""
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.TimeoutException, httpx.TimeoutException,
                httpx.Response(status_code=200, text="<p>Mock timeout retry success on third attempt HTML.</p>")
            ]
        )
        response = await fetch_html(url=valid_base_url, crawl_timeout=5)
        assert response == "<p>Mock timeout retry success on third attempt HTML.</p>"
        assert my_route.call_count == 3
    async def test_timeouts_once_succeeds_on_second_attempt(self, respx_mock):
        """Confirm that if the network speeds up right after one timeout, it successfully finishes on the second try."""
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.TimeoutException,
                httpx.Response(status_code=200, text="<p>Mock timeout retry success on second attempt HTML.</p>")
            ]
        )
        response = await fetch_html(url=valid_base_url, crawl_timeout=5)
        assert response == "<p>Mock timeout retry success on second attempt HTML.</p>"
        assert my_route.call_count == 2