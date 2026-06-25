import httpx
import logging
from graphcrawl_ai.exceptions.extration.html_from_url_exceptions import(
    InvalidUrl,
    HTTPStatusError,
    ProtocolError,
    NetworkError,
    RetryTimeoutError
)

# Basic logging configuration will replace it with proper logging in future.
logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s | %(message)s"
)

def fetch_html(url: str = "", crawl_timeout: int = 30, crawl_retry: int = 3) -> str:
    """Download the raw HTML content from a given web address.

    This function connects to a website, downloads its layout and text, and returns 
    the raw page content. It includes automatic fallback systems to try loading the 
    webpage again if a timeout occurs or if the connection drops.

    Args:
        url: The link to the website you want to read.
        crawl_timeout: How many seconds to wait for the webpage to load.
        crawl_retry: How many times to try loading the webpage again if it fails.

    Returns:
        The raw text and layout string saved directly from the website.

    Note:
        This function stops and issues specific errors if the link is typed wrong, 
        if the website fails to load, or if all retry attempts are used up.
    """

    headers = {"User-Agent": "GraphCrawl/0.1.0"}
    for attempt in range(1, crawl_retry+1):
        try:
            logging.info(f"Attempt to fetch HTML from '{url}'. | Attempt = {attempt}")

            response = httpx.get(url=url, timeout=crawl_timeout, headers=headers, follow_redirects=True) 
            response.raise_for_status()

            raw_html_data = response.text
            logging.info("HTML/Data Fetched Successfully.")

            return raw_html_data
        
        except httpx.InvalidURL:
            raise InvalidUrl(url=url)
        
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            if 500 <= status_code < 600:
                if attempt==crawl_retry:
                    logging.critical(f"Maximum retry '{attempt}/{crawl_retry}' reached!!!")
                    raise HTTPStatusError(status_code=status_code, url=url)
                logging.info(f"Recieved {status_code} form {url}! Retrying...")
            else:
                raise HTTPStatusError(status_code=status_code, url=url)
                
        
        except httpx.UnsupportedProtocol:
             raise ProtocolError(url=url)
        
        except httpx.NetworkError as e:
            raise NetworkError(err_msg=e)
        
        except httpx.TimeoutException as e:
            logging.warning(f"Attempt {attempt}/{crawl_retry} failed due to time out.")
            if attempt==crawl_retry:
                logging.critical(f"Maximum retry '{attempt}/{crawl_retry}' reached!!!")
                raise RetryTimeoutError(url=url, attempt=attempt, max_retry=crawl_retry)
            logging.info("Retrying...")