import instructor
from litellm import completion, acompletion

class Client:
    """A client manager to set up structured AI connections.

    This helper class configures instructor wrappers around LiteLLM clients, 
    making it easy to communicate with your AI models either synchronously 
    or asynchronously.
    """

    def sync_client(self):
        """Set up a standard synchronous client connection.

        Returns:
            An instructor-wrapped client that pauses execution to wait for 
            the AI provider's complete response before moving to the next line.
        """
        return instructor.from_litellm(completion)

    def async_client(self):
        """Set up an asynchronous, background-capable client connection.

        Returns:
            An instructor-wrapped client that can handle requests in the background 
            without freezing or locking up your application's execution flow.
        """
        return instructor.from_litellm(acompletion)