from abc import ABC

class LLMError(Exception, ABC):
    """The main error that happens when talking to an AI provider fails.

    This acts as the base container for all specific issues that might 
    come up while sending requests or receiving answers from an AI engine.
    """
    __module__ = "graphcrawl_ai"
    pass

class LLMAuthenticationError(LLMError):
    """The AI provider did not recognize your login details.

    This error happens when your API key is missing, typed wrong, or expired, 
    blocking access to the AI service.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM provider Authentication failed! "
                "Please check your API key (and API Base URL if provider requires)."
            )
        super().__init__(message)

class LLMTimeoutError(LLMError):
    """The AI provider took too long to answer.

    This error happens when the connection times out because the AI engine 
    is taking longer than the maximum allowed time to complete your request.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Timeout! retried maximum times"
            )
        super().__init__(message)

class LLMRetryError(LLMError):
    """The task failed completely after trying multiple times.

    This error happens when the system tries to fix a temporary problem by 
    repeating the request, but still fails after all retry attempts are exhausted.
    """
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
    """You have sent too many requests to the AI provider too quickly.

    This error happens when you exceed the allowed speed limit set by the AI 
    company, meaning you need to slow down and wait a bit before sending more data.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Rate-Limit! The provider raised rate-limit on this request. "
                "Please try again later."
            )
        super().__init__(message)

class LLMContextWindowExceededError(LLMError):
    """The website text is too large for the AI to read at once.

    This error happens when the amount of text sent to the AI exceeds its maximum 
    memory storage limit for a single conversation snippet.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Context Window Exceeded!"
            )
        super().__init__(message)

class LLMUnavailabeError(LLMError):
    """The AI provider's service is temporarily down.

    This error happens when the AI company's servers are experiencing a temporary 
    outage, maintenance downtime, or are overloaded with other users.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "LLM Unavailable! The provider service is currently unavailabe. "
                "Please try again later."
            )
        super().__init__(message)

class APIError(LLMError):
    """A general connection system issue happened on the provider's side.

    This error happens when the AI system returns a generic communication error 
    that doesn't fall into standard categories like rate limits or timeouts.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "An unexpected API Error occured. "
                "Please check your API-key or contact your provider."
            )
        super().__init__(message)

class LLMUnknownError(LLMError):
    """An unexpected error occurred that could not be recognized.

    This is a safety-net error that catches unexplained, rare problems 
    during the AI extraction phase.
    """
    __module__ = "graphcrawl_ai"
    def __init__(self, message:any = None):
        if message is None:
            message = (
                "An unexpected error occured during LLM extraction!"
            )
        super().__init__(message)