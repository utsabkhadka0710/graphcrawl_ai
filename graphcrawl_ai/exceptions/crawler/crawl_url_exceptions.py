from abc import ABC

class CrawlError(Exception, ABC):
    """
    Base class for all exceptions related to the 'crawl_url()' feature.
    
    All custom crawler errors should inherit from this class to allow for 
    uniform error handling across the library.
    """
    __module__ = 'graphcrawl_ai'
    pass

class UrlMissingError(CrawlError):
    """
    Raised when the required 'source' (URL) parameter is missing or empty.

    Action: Ensure a valid URL string is passed to the 'source' argument.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message: any = None):
        if message is None:
            message = (
                "'source' is missing or empty in crawl_url(). "
                "Expected usage: crawl_url(source='https://example.com', ...)"
            )
        super().__init__(message)

class PromptMissingError(CrawlError):
    """
    Raised when both 'prompt' and 'quick_option' arguments are missing or empty.

    Action: Provide either a custom string for 'prompt' or select a valid 
    'quick_option' to define the extraction goals.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message: any = None):
        if message is None:
            message = (
                "Both 'prompt' and 'quick_option' are missing. "
                "You must provide at least one of these to instruct the AI."
            )
        super().__init__(message)

class ResponseSchemaMissingError(CrawlError):
    """The formatting layout template for your custom prompt is missing or wrong.

    This error happens when you provide your own custom extraction prompt but 
    forget to include a valid Pydantic template model to guide the layout of the AI's response.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                f"The 'response_schema' is missing/empty or invalid schema provided. "
                f"Expected a Pydantic model/schema, please try again with a valid Pydantic model/schema."
            )
        super().__init__(message)

class InvalidDataError(CrawlError):
    """
    Raised when a parameter contains an unsupported data type or value 
    that cannot be processed by the crawler.

    Attributes:
        param_name (str): The name of the parameter that failed validation.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, param_name: str = "unknown", message: any = None):
        self.param_name = param_name
        if message is None:
            message = f"Invalid data provided for parameter: '{param_name}'."
        super().__init__(message)