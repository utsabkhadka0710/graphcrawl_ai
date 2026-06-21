import instructor
from litellm import completion, acompletion

class CLIENT:
    def sync_client(self):
        return instructor.from_litellm(completion)
    def async_client():
        return instructor.from_litellm(acompletion)
