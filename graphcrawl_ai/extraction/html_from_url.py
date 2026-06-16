import httpx
import logging

# Basic logging configuration will replace it with proper logging in future.
logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s | %(message)s"
)

class FetchError(Exception): pass

def fetch_html(url: str = "", crawl_timeout: int = 30, crawl_retry: int = 3) -> str:
    """Download the raw HTML content from a given web address.

    This function attempts to retrieve the webpage content by performing
    a GET request with a custom user agent. It includes built-in retry
    logic to handle temporary network or timeout issues.

    Args:
        url: The web address to fetch content from.
        crawl_timeout: The maximum time in seconds to wait for a response.
        crawl_retry: The number of times to try fetching if a request fails.

    Returns:
        The raw HTML string fetched from the URL.

    Note:
        The function raises a FetchError if the URL is invalid, returns an 
        HTTP error code, or fails after all retry attempts are exhausted.
    """

    headers = {"User-Agent": "GraphCrawl/0.1.0"}
    for attempt in range(crawl_retry):
        try:
            logging.info(f"Attempt to fetch HTML from '{url}'. | Attempt = {attempt+1}")

            response = httpx.get(url=url, timeout=crawl_timeout, headers=headers, follow_redirects=True) 
            response.raise_for_status()

            raw_html_data = response.text
            logging.info("HTML/Data Fetched Successfully.")

            return raw_html_data
        
        except httpx.InvalidURL as e:
             logging.error(f"Invalid URL provided! | {e}")
             raise FetchError(f"Invalid URL! '{url}'")
        
        except httpx.HTTPStatusError as e:
             logging.error(f"Received error HTTP status code '4XX/5XX' | {e}")
             raise FetchError(f"HTTP status code error, received {e.response.status_code} status code from '{url}'.")
        
        except httpx.UnsupportedProtocol as e:
             logging.error(f"Given URl is missing 'http://' or 'https://' protocol | {e}")
             raise FetchError(f"Given URl '{url}' is missing 'http://' or 'https://' protocol.")
        
        except httpx.NetworkError as e:
            logging.error(f"Network error: {e}")
            raise FetchError(f"Network error '{url}'.\nError: {e}")
        
        except httpx.TimeoutException as e:
             logging.warning(f"Attempt {attempt+1}/{crawl_retry} failed due to time out.")
             logging.info("Retrying...")
             if attempt==crawl_retry-1:
                logging.critical(f"Maximum retry '{attempt+1}/{crawl_retry}' reached!!!")
                raise FetchError(f"Timeout! retried maximum times couldn't fetch HTML for given URL '{url}' try again later.")