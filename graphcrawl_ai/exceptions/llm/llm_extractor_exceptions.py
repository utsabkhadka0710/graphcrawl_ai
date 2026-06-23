from abc import ABC

class LLMError(Exception, ABC):
    __module__ = "graphcrawl_ai"
    pass

class LLMAuthenticationError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM provider Authentication failed! "
                "Please check your API key (and API Base URL if provider requires)."
            )
        super().__init__(message)

class LLMTimeoutError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Timeout! retried maximum times"
            )
        super().__init__(message)

class LLMRetryError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM extraction operation failed after the maximum number of retry attempts. "
                "This error is likely related to the provider. "
                "Please try again later or contact the provider's customer support if this issue persists."
            )
        super().__init__(message)

class LLMRateLimitError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Rate-Limit! The provider raised rate-limit on this request. "
                "Please try again later."
            )
        super().__init__(message)

class LLMContextWindowExceededError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Context Window Exceeded!"
            )
        super().__init__(message)

class LLMUnavailabeError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Unavailable! The provider service is currently unavailabe. "
                "Please try again later."
            )
        super().__init__(message)

class APIError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "An unexpected API Error occured. "
                "Please check your API-key or contact your provider."
            )
        super().__init__(message)

class LLMUnknownError(LLMError):
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "An unexpected error occured during LLM extraction!"
            )
        super().__init__(message)