import httpx
import logging

# Basic logging configuration will replace it with proper logging in future.
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(message)s"
)

class FetchError(Exception): pass

def fetch_html(url: str = "", timeout: float = 30, retry: int = 3) -> str:
    """Fetch raw HTML content from a specified URL with retry logic.

    This function dispatches synchronous HTTP GET requests to retrieve web content,
    automatically resolving redirects. It isolates the pipeline from connection 
    instability by implementing a retry mechanism specifically for timeout failures 
    and translates lower-level network exceptions into unified high-level errors.

    Args:
        url: The target web address to request data from.
        timeout: The maximum duration in seconds to wait for a server response.
        retry: The maximum number of connection attempts to make in case of timeouts.

    Returns:
        The raw HTML string content fetched from the target URL.

    Raises:
        FetchError: If the URL is structurally malformed, missing its protocol,
            encounters a non-200 HTTP status code, experiences general network 
            failures, or exhausts all retry attempts following continuous timeouts.
    """

    headers = {"User-Agent": "GraphCrawl/0.1.0"}
    for attempt in range(retry):
        try:
            logging.info(f"Attempt to fetch HTML from '{url}'. | Attempt = {attempt+1}")

            response = httpx.get(url=url, timeout=timeout, headers=headers, follow_redirects=True) 
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
             logging.warning(f"Attempt {attempt+1}/{retry} failed due to time out.")
             logging.info("Retrying...")
             if attempt==retry-1:
                logging.critical(f"Maximum retry '{attempt+1}/{retry}' reached!!!")
                raise FetchError(f"Timeout! retried maximum times couldn't fetch HTML for given URL '{url}' try again later.")