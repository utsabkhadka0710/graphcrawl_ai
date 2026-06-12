from abc import ABC
class CrawlError(Exception, ABC):
    __module__ = 'graphcrawl_ai'
    """Base class for exception related to calling feature 'crawl_url()"""
    pass

class UrlMissingError(CrawlError):
    """Raised when the requied URL source parameter is missing or is empty"""
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any=None):
        if message is None:
            message = (
                "'source' is missing or is empty in crawl_url(), "
                "Expected: crawl_url(source='http://example.com', ...)\n"
                "Please enter a valid URL string in 'source' parameter."
            )
            super().__init__(message)


class PromptMissingError(CrawlError):
    """Raises when the one of either prompt or quick_option is missing or is empty"""
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any=None):
        if message is None:
            message = (
                "both 'prompt' and 'quick_option' are missing or are empty in crawl_url(), "
                "Expected: crawl_url(source='https://example.com', prompt='Extraction prompt here...') "
                "or crawl_url(source='https://example.com', quick_option='Available QuickOption')\n"
                "please enter a custom extraction prompt or select one of available quick_option"
            )
        super().__init__(message)

