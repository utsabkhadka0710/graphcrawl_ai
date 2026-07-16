import instructor
from litellm import completion, acompletion

class Client:
    """A client manager to set up structured AI connections.

    This helper class configures instructor wrappers around LiteLLM clients, 
    making it easy to communicate with your AI models either synchronously 
    or asynchronously.
    """

    def get_client(self):
        """Set up an asynchronous, background-capable client connection.

        Returns:
            An instructor-wrapped client that can handle requests in the background 
            without freezing or locking up your application's execution flow.
        """
        return instructor.from_litellm(acompletion, async_client=True)