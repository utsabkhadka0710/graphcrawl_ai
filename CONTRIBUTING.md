# Contributing to GraphCrawl AI

Thanks for your interest in contributing! This guide covers how to get the project running locally, how the code is organized, and how to submit changes.

GraphCrawl AI is in early alpha, so the API and internals are still changing. If you're planning something big, please open an issue first so we can agree on the direction before you spend time on it.

## Table of contents

- [Getting started](#getting-started)
- [How the code is organized](#how-the-code-is-organized)
- [Development workflow](#development-workflow)
- [Code conventions](#code-conventions)
- [Adding a new quick option](#adding-a-new-quick-option)
- [Supporting a new LLM provider](#supporting-a-new-llm-provider)
- [Testing](#testing)
- [Changing dependencies](#changing-dependencies)
- [Submitting a pull request](#submitting-a-pull-request)
- [Reporting bugs](#reporting-bugs)

## Getting started

**Prerequisites:** Python 3.11 or newer, and an API key for any LLM provider supported by [LiteLLM](https://docs.litellm.ai/docs/providers). You only need a key to run the live demo; the test suite works without one.

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/<your-username>/graphcrawl_ai.git
cd graphcrawl_ai

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1

# 3. Install the pinned dependencies, then the project itself
pip install -r requirements-lock.txt
pip install -e . --no-deps

# 4. (Optional) set up credentials for the live demo
cp .env.example .env
# Edit .env and add the key that matches your provider, e.g. GEMINI_API_KEY
```

The lock file pins every dependency to the versions the project is tested with and includes the test tools, so `pytest` works right away. Please develop against it unless you are specifically testing newer versions.

Check everything works:

```bash
pytest graphcrawl_ai/tests/
```

## How the code is organized

A call to `crawl_url()` flows through these layers:

```
crawl_url()                         crawler/crawl_url.py
  ├─ validates input, builds a UrlExtractionRequest
  ├─ resolve_url_request()          resolver/url_resolver.py
  │    ├─ fetch_html()              extraction/html_from_url.py   (httpx + retries)
  │    ├─ extract_content_from_html()  extraction/text_from_html.py  (bs4 + lxml)
  │    └─ picks prompt + response schema (llm/prompts.py, models/.../response_models)
  └─ llm_extract()                  llm/engine.py                 (Instructor + LiteLLM)
```

| Path | Responsibility |
|---|---|
| `graphcrawl_ai/crawler/` | The public entry point, `crawl_url()` |
| `graphcrawl_ai/extraction/` | Fetching HTML and cleaning it down to text |
| `graphcrawl_ai/resolver/` | Turning a user request into an LLM job (prompt + schema + content) |
| `graphcrawl_ai/llm/` | The LLM client, engine, built-in prompts, and error mapping |
| `graphcrawl_ai/models/crawl_url/` | Pydantic request and response models |
| `graphcrawl_ai/exceptions/` | Custom exceptions for the crawler, fetcher, and LLM layers |
| `graphcrawl_ai/utils/` | Small helpers such as `safe_cast` |
| `graphcrawl_ai/tests/` | The pytest suite |
| `api/` | FastAPI skeleton (health checks only for now) |
| `examples/` | Usage examples |

## Development workflow

Use feature branches and never commit directly to `main`.

```bash
git checkout -b feature/your-feature-name

# make your changes, then
git add .
git commit -m "feat: short description of what changed"

git push origin feature/your-feature-name
```

Commit message prefixes: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.

## Code conventions

**Type hints everywhere.** All function signatures need parameter and return type annotations.

```python
# Good
async def fetch_html(url: str = "", crawl_timeout: int = 30, crawl_retry: int = 3) -> str:

# Bad
async def fetch_html(url, timeout, retry):
```

**Pydantic models at layer boundaries.** Data passed between layers (user to resolver, resolver to LLM engine, LLM engine back to the user) should be a Pydantic `BaseModel`, not a raw dict.

**Docstrings on public functions and classes.** Follow the existing style: a one-line summary, a blank line, then `Args:`, `Returns:`, and optionally `Raises:` or `Note:`.

```python
def my_function(param: str) -> str:
    """One-line summary.

    Longer description if needed.

    Args:
        param: What this parameter does.

    Returns:
        What the function returns.
    """
```

**Keep the layers separate.** The fetcher knows nothing about Pydantic schemas or LLMs. The LLM engine knows nothing about HTML. The resolver is the one place that touches both, and that is intentional.

**Raise specific exceptions.** Add a clear exception class in `graphcrawl_ai/exceptions/` rather than raising a bare `Exception` or `ValueError`.

**No secrets in code.** API keys go in `.env` or your shell environment, never in source files, tests, or examples.

## Adding a new quick option

Quick options (`summary`, `contacts`, `products`) are built-in modes with their own prompt and response schema. Adding one touches four files. This example adds an `events` option.

**1. Register the option.** In `graphcrawl_ai/models/crawl_url/request_models/user_request.py`, add it to **both** the enum and the `Literal` type:

```python
class QuickOption(str, Enum):
    SUMMARY = "summary"
    CONTACTS = "contacts"
    PRODUCTS = "products"
    EVENTS = "events"            # new

AvailableQuickOption = Literal["summary", "contacts", "products", "events"]   # new
```

**2. Write the prompt.** In `graphcrawl_ai/llm/prompts.py`:

```python
events = """You are a backend API. Extract all events from the text inside <page_content>. \
You must respond strictly with a valid JSON object. Do not include markdown or conversational text. \
JSON Schema: {"status": "success", "events": [{"name": "", "date": ""}]}"""
```

**3. Add the response model.** In `graphcrawl_ai/models/crawl_url/response_models/llm_response.py`:

```python
class EventItem(BaseModel):
    name: str
    date: str

class UrlEventsResponse(UrlBaseResponse):
    events: list[EventItem]
```

**4. Wire it into the resolver.** In `graphcrawl_ai/resolver/url_resolver.py`, import `UrlEventsResponse` and add a case:

```python
case QuickOption.EVENTS:
    prompt = prompts.events
    response_schema = UrlEventsResponse
```

`crawl_url(quick_option="events", ...)` now works. Then:

- add tests (see [Testing](#testing)),
- add the option to the quick options table in `README.md`.

> **Heads up:** the existing prompts tell the model to return `"status": "error"` on a safety-policy violation, but `UrlBaseResponse.status` only allows `"success"` or `"failure"`. This is a known issue, so don't copy that line into new prompts until it is fixed.

## Supporting a new LLM provider

Provider support comes from [LiteLLM](https://docs.litellm.ai/docs/providers), so there is usually no new backend code to write. Any model string LiteLLM accepts is passed straight through. What helps most is **verifying** a provider:

1. Run `examples/live_demo_example.py` (or a `quick_option` call) with the provider's `model` string and key.
2. Check that the structured output comes back valid.
3. Open a PR or issue noting the provider and model, and add it to the model table in `README.md`.

If the provider raises error types that end up as `LLMUnknownError`, extend `_map_exceptions()` in `graphcrawl_ai/llm/engine.py` and add a test for it.

## Testing

Run the whole suite with:

```bash
pytest graphcrawl_ai/tests/
```

The tests **must not call real websites or real LLMs**. Follow the patterns already in the suite:

- Mark async tests with `@pytest.mark.asyncio`.
- Mock HTTP with [`respx`](https://lundberg.github.io/respx/) (see `test_fetch_html.py`).
- Mock the LLM client with `unittest.mock.patch` / `AsyncMock` (see `test_llm_engine.py`).
- Use `@pytest.mark.parametrize` for input variations.
- Put new tests in `graphcrawl_ai/tests/test_<area>.py`.

When contributing, please:

- add or update a test that exercises the code path you changed,
- make sure the full suite passes before opening a PR,
- for a new quick option, add a test that checks it routes to the right prompt and schema.

For a manual smoke test against a real provider, use `examples/live_demo_example.py`. It makes a real network request and a real LLM call, so it is not part of the automated suite.

## Changing dependencies

If you add or upgrade a dependency:

1. Update `pyproject.toml`.
2. Regenerate `requirements-lock.txt` from a clean environment and confirm the tests pass. The steps are in the README under [Updating the lock file](README.md#updating-the-lock-file), including re-adding the `uvloop` platform marker.
3. Mention the change in your PR description.

## Submitting a pull request

1. Make sure your branch is up to date with `main`.
2. Run `pytest graphcrawl_ai/tests/` and confirm everything passes.
3. Write a clear description of what you changed and why.
4. Reference related issues (for example `Closes #42`).
5. Keep PRs focused. One logical change per PR is easier to review.
6. Be responsive to review feedback; maintainers may ask for changes before merging.

## Reporting bugs

Open an issue on GitHub and include:

- the URL you were trying to crawl, or a minimal reproduction,
- the `quick_option` or `prompt` you used, and the `model` string (never your API key),
- the full error message and traceback,
- your Python version and operating system.

Feature requests are welcome too. Describe the use case, not just the solution.