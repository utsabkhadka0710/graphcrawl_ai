from abc import ABC

class FetchError(Exception, ABC):
    """The main error that happens when loading a webpage fails.

    This acts as the base container for all specific issues that might 
    come up while downloading a website's content.
    """
    __module__ = "graphcrawl_ai"
    pass

class InvalidUrl(FetchError):
    """The provided website link is not written correctly.

    This error happens when the address format is broken or typed wrong, 
    making it impossible to visit.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, url:str, message:any=None):
        if message is None:
            message = (
                f"Invalid URL provided! '{url}' is an invalid URL\n"
                "Please try again with valid URL."
            )
        super().__init__(message)

class HTTPStatusError(FetchError):
    """The website sent back a failure error code.

    This error happens when the website server responds with an error code 
    (like a 404 page not found or a 500 server error), meaning we couldn't 
    get the content.
    """
    __module__ = "graphcrawl_ai.fetch_html"
    def __init__(self, status_code:int, url:str, message:any=None):
        if message is None:
            message = (
                f"HTTP status code '4xx/5xx' error, received '{status_code}' status code from '{url}'."
            )
        super().__init__(message)

class ProtocolError(FetchError):
    """The website link is missing its web protocol prefix.

    This error happens when a link does not start with 'http://' or 'https://', 
    which the system needs to know how to connect to the site.
    """
    __module__ = "graphcrawl_ai_fetch_html"
    def __init__(self, url:str, message:any=None):
        if message is None:
            message = (
                f"Given URl '{url}' is missing 'http://' or 'https://' protocol."
            )
        super().__init__(message)

class NetworkError(FetchError):
    """A general connection or internet issue occurred.

    This error happens when there is a physical connection issue, DNS failure, 
    or any other low-level network interruption blocking the request.
    """
    __module__ = "graphcrawl_ai.fetch_html"
    def __init__(self, err_msg:str, message:any=None):
        if message is None:
            message = (
                f"Network Error: {err_msg}"
            )
        super().__init__(message)

class RetryTimeoutError(FetchError):
    """The system gave up trying after the webpage took too long to load.

    This error happens when the website takes too long to respond, and the 
    system has already tried loading it the maximum allowed number of times.
    """
    __module__ = "graphcrawl_ai.fetch_html"
    def __init__(self, url:str, attempt:int, max_retry:int, message:any=None):
        if message is None:
            message =(
                f"Timeout! retried maximum times '{attempt}/{max_retry}'couldn't fetch HTML for given URL '{url}' try again later."
            )
        super().__init__(message)