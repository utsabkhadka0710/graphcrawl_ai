import pytest
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
@pytest.mark.parametrize(
    "status_code",
    [200, 203, 206,],
    ids = ["status-code-200-OK", "status-code-203-Non-Authoritative Information", "status-code-206-Partial Content"]
)
def test_fetch_html_return_html(status_code):
    my_route = respx.get(url=valid_base_url).mock(
        return_value=httpx.Response(status_code=status_code, text="<p>Mock success HTML.</p>")
    )  
    response = fetch_html(url=valid_base_url)
    assert my_route.called
    assert my_route.call_count == 1
    assert response == "<p>Mock success HTML.</p>"


@respx.mock
@pytest.mark.parametrize(
    "status_code",
    [400, 401, 403, 404, 408,429,],
    ids = ["status-code-400-Bad Request", "status-code-401-Unauthorized", "status-code-403-Forbidden",
           "status-code-404-Not Found", "status-code-408-Request Timeout", "status-code-429- Too Many Requests"]
)
def test_fetch_html_non_retriable_client_errors(status_code):
    my_route = respx.get(url=valid_base_url).mock(return_value=httpx.Response(status_code=status_code))
    with pytest.raises(HTTPStatusError):
        fetch_html(url=valid_base_url)
    assert my_route.called
    assert my_route.call_count == 1


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
    def test_fails_all_three_retries(self, status_code, respx_mock):
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[httpx.Response(status_code)]*3
        )
        with pytest.raises(HTTPStatusError):
            fetch_html(url=valid_base_url, crawl_retry=3)
        assert my_route.call_count == 3
    def test_fails_twice_succeeds_last_retry(self, status_code, respx_mock):
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.Response(status_code), httpx.Response(status_code),
                httpx.Response(status_code=200, text="<p>Mock retry success on third attempt HTML.</p>")
            ]
        )
        response = fetch_html(url=valid_base_url, crawl_retry=3)
        assert response == "<p>Mock retry success on third attempt HTML.</p>"
        assert my_route.call_count == 3
    def test_fails_once_succeeds_on_second_attempt(self, status_code, respx_mock):
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.Response(status_code),
                httpx.Response(status_code=200, text="<p>Mock retry success on second attempt HTML.</p>")
            ]
        )
        response = fetch_html(url=valid_base_url, crawl_retry=3)
        assert response == "<p>Mock retry success on second attempt HTML.</p>"
        assert my_route.call_count == 2

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
def test_fetch_html_protocol_error(malformed_or_protocol_missing_url):
    with pytest.raises(ProtocolError):
        fetch_html(url=malformed_or_protocol_missing_url)


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
def test_fetch_html_malformed_or_invalid_url(malformed_or_invalid_url):
    with pytest.raises(InvalidUrl):
        fetch_html(url=malformed_or_invalid_url)

@respx.mock
def test_fetch_html_network_error():
    my_route = respx.get(url=valid_base_url).mock(side_effect=httpx.NetworkError(message="Mock NetworkError"))
    with pytest.raises(NetworkError):
        fetch_html(url=valid_base_url)
    assert  my_route.called
    assert my_route.call_count == 1

class TestFetchHtmlTimeout:
    def test_timeouts_all_three_retries(self, respx_mock):
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[httpx.TimeoutException]*3
        )
        with pytest.raises(RetryTimeoutError):
            fetch_html(url=valid_base_url, crawl_timeout=5)
        assert my_route.call_count == 3
    def test_timeouts_twice_succeeds_on_last_attempt(self, respx_mock):
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.TimeoutException, httpx.TimeoutException,
                httpx.Response(status_code=200, text="<p>Mock timeout retry success on third attempt HTML.</p>")
            ]
        )
        response = fetch_html(url=valid_base_url, crawl_timeout=5)
        assert response == "<p>Mock timeout retry success on third attempt HTML.</p>"
        assert my_route.call_count == 3
    def test_timeouts_once_succeeds_on_second_attempt(self, respx_mock):
        my_route = respx_mock.get(url=valid_base_url).mock(
            side_effect=[
                httpx.TimeoutException,
                httpx.Response(status_code=200, text="<p>Mock timeout retry success on second attempt HTML.</p>")
            ]
        )
        response = fetch_html(url=valid_base_url, crawl_timeout=5)
        assert response == "<p>Mock timeout retry success on second attempt HTML.</p>"
        assert my_route.call_count == 2