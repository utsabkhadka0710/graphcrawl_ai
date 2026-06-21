import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class ModelSpec:
    model: str
    max_retry: int
    fallbacks: list[str] = field(default_factory=list)
    

def resolve_model():
    pass


def build_kwargs(llm_config):
    pass