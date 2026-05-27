import httpx
import logging

# Basic logging configuration will replace it with proper logging in future.
logging.basicConfig(
    level = logging.INFO,
    format = "| %(asctime)s | %(levelname)s | %(message)s |"
)

class FetchError(Exception): pass

"""
Raw HTML fetcher

Handles:
- reuests timeout
- retry attempts on request timeouts
- invalid URL error
- HTTP error
- network error
- protocol error
- status (4XX/5XX) code error

Returns raw HTML on fetching success for given URL.

Raises http, protocol, network, timeout and various edge cases Excetions and error during HTML fetching for a given URL.
"""
def fetch_html(url:str = "", timeout:float = 5, retry:int = 3) -> str:

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
             raise FetchError(f"HTTP status code error, received {e.response.status_code} staus code from '{url}'.")
        
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
                raise FetchError(f"Timeout! retried maximum tried couldn't fetch HTML for given URL '{url}' try again later.")
