# Contributing to graphcrawl_ai

Thank you for your interest in contributing! This document explains how to get the project running locally, the conventions the codebase follows, and the process for submitting changes.

---

## Table of contents

- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Development workflow](#development-workflow)
- [Code conventions](#code-conventions)
- [Adding a new quick option](#adding-a-new-quick-option)
- [Adding a new LLM backend](#adding-a-new-llm-backend)
- [Testing](#testing)
- [Submitting a pull request](#submitting-a-pull-request)
- [Reporting bugs](#reporting-bugs)

---

## Getting started

**Prerequisites:** Python ≥ 3.11, a [Gemini API key](https://aistudio.google.com/app/apikey).

```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/graphcrawl_ai.git
cd graphcrawl_ai

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install in editable mode with all dependencies
pip install -e .

# 4. Set up your environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API key
```

---

## Project structure

Understanding the data flow helps you find the right place to make changes.

```
URL input
  └─→ crawl.py            crawl_url() — public entry point, composes everything
        └─→ request_resolver/
              user_url_request_resolver.py
                  ├─→ crawler/fetcher.py       HTTP fetch (httpx, retry logic)
                  ├─→ extraction/parser.py     HTML → clean text (bs4 + lxml)
                  └─→ llm/prompts.py           Built-in prompt strings
        └─→ llm/gemini_extractor.py            Gemini API call, response parsing
              └─→ models/response_models/      Typed Pydantic output schemas
```

**Key directories:**

| Path | Responsibility |
|---|---|
| `graphcrawl_ai/crawl.py` | Single public function, wires everything together |
| `graphcrawl_ai/crawler/` | HTTP layer — fetching and retry |
| `graphcrawl_ai/extraction/` | HTML cleaning and text normalization |
| `graphcrawl_ai/llm/` | LLM client, prompts, and request routing |
| `graphcrawl_ai/models/` | All Pydantic request and response schemas |
| `api/` | FastAPI REST interface (under development) |
| `tests/` | Test scripts |
| `examples/` | Usage examples |

---

## Development workflow

Use feature branches. Never commit directly to `main`.

```bash
# Create a branch for your work
git checkout -b feature/your-feature-name

# Make your changes, then commit
git add .
git commit -m "feat: short description of what changed"

# Push and open a pull request
git push origin feature/your-feature-name
```

Commit message prefixes: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.

---

## Code conventions

**Type hints everywhere.** All function signatures must include parameter and return type annotations.

```python
# Good
def fetch_html(url: str, crawl_timeout: float = 30, crawl_retry: int = 3) -> str:

# Bad
def fetch_html(url, timeout, retry):
```

**Pydantic models for all data boundaries.** Any data that crosses a layer boundary (user → resolver, resolver → LLM, LLM → user) must be a Pydantic `BaseModel`. No raw dicts passed between layers.

**Docstrings on all public functions and classes.** Use the existing style — one-line summary, blank line, `Args:`, `Returns:`, optional `Note:` block.

```python
def my_function(param: str) -> str:
    """One-line summary.

    Longer description if needed.

    Args:
        param: What this parameter does.

    Returns:
        What the function returns.

    Note:
        Any caveats or requirements.
    """
```

**Keep layers separate.** The fetcher must not know about Pydantic schemas. The LLM extractor must not know about HTML. The resolver is the only place that touches both — that's intentional.

**No secrets in code.** API keys and credentials go in `.env` only. Never hardcode them.

---

## Adding a new quick option

Quick options are the four built-in modes (`summary`, `contacts`, `products`, `auto`). To add a new one, you need to touch four files:

**1. Add the enum value** — `graphcrawl_ai/models/request_models/crawl_url_models/request_url_user.py`

```python
class QuickOption(str, Enum):
    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    AUTO = "auto"
    EVENTS = "events"   # ← new
```

**2. Write the prompt** — `graphcrawl_ai/llm/prompts.py`

```python
events = """You are a backend API. Extract all events from the text inside <page_content>. \
Return a valid JSON object only. No markdown, no preamble. \
JSON Schema: {"status": "success", "events": [{"name": "", "date": "", "location": "", "description": ""}]}"""
```

**3. Add the response model** — `graphcrawl_ai/models/response_models/crawl_url_models/response_url_llm.py`

```python
class EventItem(BaseModel):
    name: str
    date: str
    location: str
    description: str

class UrlEventsResponse(UrlBaseResponse):
    events: list[EventItem]
```

**4. Wire it in the resolver** — `graphcrawl_ai/llm/request_resolver/user_url_request_resolver.py`

```python
case QuickOption.EVENTS:
    prompt = prompts.events
    response_schema = UrlEventsResponse
```

That's it. The public `crawl_url()` function will now accept `quick_option="events"`.

---

## Adding a new LLM backend

The project currently only supports Gemini (via `google-genai`). To add support for another provider:

1. Create a new file at `graphcrawl_ai/llm/your_provider_extractor.py` following the same interface as `gemini_extractor.py`:

```python
def get_response_your_provider(
    request: ExtractionRequestToLLM,
    response_schema: type[ResponseSchema]
) -> ResponseSchema:
    ...
```

2. The function must accept an `ExtractionRequestToLLM` and a Pydantic model class, and return a validated instance of that class.

3. Update `crawl_url()` in `crawl.py` to accept a `backend` parameter and route to the right extractor.

4. Add any new dependencies to `pyproject.toml` under `[project.dependencies]`.

---

## Testing

The current test suite lives in `tests/test_init.py` and performs a live integration test against a real URL. Running it requires a valid `GEMINI_API` key in your `.env`.

```bash
python tests/test_init.py
```

When contributing, please:

- Add a test that exercises the code path you changed.
- If your change adds a new quick option, include a live test URL where that option produces a meaningful result.
- If your change is purely internal (a refactor, error message update, etc.), verify that the existing test still passes.

Unit tests that mock the HTTP and LLM layers are welcome and encouraged — the project would benefit from a proper `pytest`-based test suite as it grows.

---

## Submitting a pull request

1. Make sure your branch is up to date with `main` before opening the PR.
2. Write a clear description of what you changed and why.
3. Reference any related issues (e.g. `Closes #42`).
4. Keep PRs focused — one logical change per PR is easier to review than a large mixed change.
5. Be responsive to review feedback; maintainers may ask for changes before merging.

---

## Reporting bugs

Open an issue on GitHub and include:

- The URL you were trying to crawl (or a minimal reproduction)
- The `quick_option` or `prompt` you used
- The full error message and traceback
- Your Python version and operating system

Feature requests are welcome too — describe the use case, not just the solution.