# GraphCrawl AI 🕷️🕸️

> AI-powered web scraping and structured data extraction — currently under active development.

⚠️ **This project is workable but not production-ready yet.** Core extraction works end-to-end, but the API and internals are still being refined and will keep changing. See [Known limitations](#known-limitations-current-state) before relying on it.

---

## What is it?

GraphCrawl AI is a Python library that turns any public webpage into structured, typed data using AI. You point it at a URL, tell it what you want (or let it decide), and get back a clean Pydantic model — no HTML parsing boilerplate, no prompt engineering required.

---

## How it works

```
URL → HTTP fetch → HTML cleaning → LLM (via instructor + litellm) → Pydantic response object
```

1. **Fetcher** (`graphcrawl_ai/extraction/html_from_url.py`) — downloads the raw HTML with retry and timeout logic (`httpx`)
2. **Parser** (`graphcrawl_ai/extraction/text_from_html.py`) — strips noise tags (scripts, nav, footer, ads) and normalizes whitespace (`beautifulsoup4` + `lxml`)
3. **Resolver** (`graphcrawl_ai/resolver/url_resolver.py`) — picks the right prompt and response schema based on your chosen mode, then fetches and cleans the page
4. **LLM engine** (`graphcrawl_ai/llm/engine.py`) — sends the clean text to your chosen model through [`instructor`](https://python.useinstructor.com/) (wrapping [`litellm`](https://docs.litellm.ai/)) and parses the JSON response back into a typed Pydantic model

Because extraction goes through `litellm`, GraphCrawl AI can talk to any provider `litellm` supports (Gemini, OpenAI, Anthropic, etc.) — you just need to pass the right `model` string and credentials. See [Choosing a model](#choosing-a-model) below.

---

## Requirements

- Python ≥ 3.11
- An API key for whichever LLM provider/model you pass to `crawl_url()`

---

## Installation

install from source:

```bash
git clone https://github.com/your-username/graphcrawl_ai.git
cd graphcrawl_ai
```
initialize the virtual environment and pip install editable graphcrawl_ai:
- MacOS/Linux
```bash
python -m venv venv
source venv/bin/activate
pip install -e . 
```
- Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -e .
```

---

## Configuration

`crawl_url()` now takes `model` and `api_key` directly, so you have two ways to supply credentials:

**Option 1 — pass `api_key` explicitly (recommended, most reliable):**

```python
result = crawl_url(
    source="https://example.com",
    quick_option="summary",
    model="gemini/gemini-2.5-flash",
    api_key="your_api_key_here",
)
```

**Option 2 — rely on environment variables:**
If you omit `api_key`, `litellm` falls back to its standard provider-prefixed environment variables (inferred from the `model` string), e.g. `GEMINI_API_KEY` for `gemini/...` models or `OPENAI_API_KEY` for `openai/...` models:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The repo's `.env.example` uses a generic `PROVIDER_API_KEY` placeholder as a reminder to set *some* provider's key — rename it to match whichever provider you're actually using (`GEMINI_API_KEY`, `OPENAI_API_KEY`, etc.), since `litellm` doesn't read a literal `PROVIDER_API_KEY` variable.

If you load env files yourself, make sure this runs before calling `crawl_url()`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Quick start

```python
from graphcrawl_ai import crawl_url

# Get a summary of any webpage
result = crawl_url(
    source="https://example.com/",
    quick_option="summary",
    model="gemini/gemini-2.5-flash",
    api_key="your_api_key_here"    
)

print(result.model_dump_json(indent=2))
print(result.summary)
print(result.key_takeaways)
```
### Output:
```JSON
{
  "status": "success",
  "summary": "This domain is designated for use in documentation examples.",
  "key_takeaways": [
    "This domain can be used in documentation examples without needing permission.",
    "It should be avoided for use in operations."
  ]
}

This domain is designated for use in documentation examples.

['This domain can be used in documentation examples without needing permission.', 'It should be avoided for use in operations.']
```

---

## Usage

### `crawl_url()`

The single public entry point for the library.

```python
crawl_url(
    source: str,
    model: str,
    prompt: str = None,
    quick_option: Literal["summary", "contacts", "products", "auto"] = None,
    api_key: str = None,
    response_schema: type[BaseModel] | None = None,
    llm_timeout: float = 60,
    llm_retry: int = 3,
    crawl_timeout: float = 30,
    crawl_retry: int = 3
) -> BaseModel
```

- `source` and `model` are required. `model` is the `litellm`-style provider/model string (e.g. `"gemini/gemini-2.5-flash"`, `"openai/gpt-4o"`).
- You must provide either `prompt` or `quick_option` — not neither (raises `PromptMissingError`). If you provide both, `prompt` wins for instructions, but if `quick_option` is also set, its associated response schema is still used unless you also pass `response_schema` explicitly.
- `api_key` is optional — omit it to let `litellm` resolve credentials from the environment instead (see [Configuration](#configuration)).

### Choosing a model

`model` is passed straight through to `litellm`, so any model string `litellm` supports should work, including (but not limited to):

| Provider | Example `model` string |
|---|---|
| Google Gemini | `"gemini/gemini-2.5-flash"` |
| OpenAI | `"openai/gpt-4o"` |
| Anthropic | `"anthropic/claude-sonnet-4-5"` |

This has only been exercised against Gemini models so far in this project's own tests — other providers should work given `litellm`'s support, but haven't been verified here yet.

### Quick options

| Option | What it extracts | Response type |
|---|---|---|
| `"summary"` | Page summary + key takeaways | `UrlSummaryResponse` |
| `"contacts"` | Emails, phones, addresses, social links | `UrlContactsResponse` |
| `"products"` | Product name, price, description, rating, units sold | `UrlProductsResponse` |
| `"auto"` | AI decides what's most useful | `UrlAutoResponse` |

### Example: extract contacts

```python
result = crawl_url(
    source="https://company.com/contact",
    quick_option="contacts",
    model="gemini/gemini-2.5-flash",
)

print(result.contact_info.emails)
print(result.contact_info.phones)
print(result.contact_info.social_links)
```

### Example: extract products

```python
result = crawl_url(
    source="https://shop.example.com/category/headphones",
    quick_option="products",
    model="gemini/gemini-2.5-flash",
)

for product in result.products:
    print(product.name, product.price)
```

### Example: custom prompt

```python
result = crawl_url(
    source="https://techblog.example.com/article",
    prompt="Extract the author name, publication date, and all external links mentioned.",
    model="gemini/gemini-2.5-flash",
)

for item in result.response:
    print(item)
```

### Example: custom response schema

Define your own Pydantic model to get exactly the shape you need:

```python
from pydantic import BaseModel
from graphcrawl_ai import crawl_url

class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    salary: str
    requirements: list[str]

result = crawl_url(
    source="https://jobs.example.com/posting/123",
    prompt="Extract the job title, company, location, salary, and requirements.",
    model="gemini/gemini-2.5-flash",
    response_schema=JobPosting
)

print(result.title)
print(result.requirements)
```

### Tuning timeouts and retries

```python
result = crawl_url(
    source="https://slow-site.example.com",
    quick_option="summary",
    model="gemini/gemini-2.5-flash",
    crawl_timeout=60,  # seconds to wait for the webpage
    crawl_retry=5,     # retry attempts for the HTTP fetch
    llm_timeout=120,   # seconds to wait for the LLM
    llm_retry=5,       # retry attempts for the LLM call
)
```

All four values are coerced to integers internally (via ceiling rounding), so floats like `crawl_timeout=2.5` are accepted and rounded up to `3`. Passing a non-numeric value raises `InvalidDataError`.

---

## Response models

All responses extend `UrlBaseResponse` which carries a `status` field (`"success"` or `"failure"`). Every response is a valid Pydantic model — call `.model_dump()` for a dict or `.model_dump_json()` for JSON.

```python
result = crawl_url(
    source="https://example.com",
    quick_option="summary",
    model="gemini/gemini-2.5-flash",
)

print(result.status)                    # "success"
print(result.model_dump())              # dict
print(result.model_dump_json(indent=2)) # pretty JSON
```

---

## Project structure

```
graphcrawl_ai-main/
├── graphcrawl_ai/
│   ├── __init__.py                                   # Public exports: crawl_url + exceptions
│   ├── crawler/
│   │   └── crawl_url.py                              # Public API: crawl_url()
│   ├── extraction/
│   │   ├── html_from_url.py                          # HTTP fetch with retry (httpx)
│   │   └── text_from_html.py                         # HTML → clean text (bs4 + lxml)
│   ├── llm/
│   │   ├── client.py                                 # instructor + litellm client setup
│   │   ├── config.py                                 # ModelSpec dataclass + unused resolve_model/build_kwargs stubs
│   │   ├── engine.py                                 # Runs the LLM extraction call (model/api_key now wired in)
│   │   └── prompts.py                                # Built-in prompts for quick options
│   ├── resolver/
│   │   └── url_resolver.py                           # Routes quick_option/prompt → fetch + schema
│   ├── models/crawl_url/
│   │   ├── request_models/
│   │   │   ├── user_request.py                       # UrlExtractionRequest, QuickOption
│   │   │   └── request_to_llm.py                     # ExtractionJobToLLM (resolver → engine)
│   │   └── response_models/
│   │       ├── llm_response.py                       # UrlSummaryResponse, UrlContactsResponse, etc.
│   │       └── parser_response.py                    # HtmlParsedContent (intermediate)
│   ├── exceptions/
│   │   ├── crawler/crawl_url_exceptions.py           # UrlMissingError, PromptMissingError, InvalidDataError
│   │   ├── extration/html_from_url_exceptions.py     # FetchError and subclasses
│   │   └── llm/llm_extractor_exceptions.py           # LLMError and subclasses
│   └── utils/
│       └── safe_cast.py                              # Numeric coercion for timeout/retry params
├── api/
│   └── main.py                                       # FastAPI app — currently just / and /health (in progress)
├── examples/
│   └── basic_usage.py                                # Empty placeholder — not yet written
├── tests/
│   └── test_init.py                                  # Live integration script (not a pytest suite yet)
├── pyproject.toml
└── .env.example
```

---

## REST API

A FastAPI application is included under `api/` and is currently a bare skeleton — it only exposes `/` and `/health`, with no crawling endpoints wired up yet. To run it locally:

```bash
uvicorn api.main:app --reload
```

---

## Error handling

Crawling and validation errors all live under `graphcrawl_ai`:

```python
from graphcrawl_ai import crawl_url, UrlMissingError, PromptMissingError, InvalidDataError, HTTPStatusError

try:
    result = crawl_url(
        source="https://example.com",
        quick_option="summary",
        model="gemini/gemini-2.5-flash",
    )
except UrlMissingError:
    print("No source URL was provided.")
except PromptMissingError:
    print("Provide either `prompt` or `quick_option`.")
except InvalidDataError as e:
    print(f"Bad value for parameter: {e.param_name}")
except HTTPStatusError as e:
    print(f"The page returned an error: {e}")
```

The HTTP-fetch errors (`InvalidUrl`, `HTTPStatusError`, `ProtocolError`, `NetworkError`, `RetryTimeoutError`) all subclass `FetchError`, importable from `graphcrawl_ai.exceptions.extration.html_from_url_exceptions`. LLM-side failures (`LLMAuthenticationError`, `LLMTimeoutError`, `LLMRetryError`, `LLMRateLimitError`, `LLMContextWindowExceededError`, `LLMUnavailabeError`, `APIError`, `LLMUnknownError`) subclass `LLMError` in `graphcrawl_ai.exceptions.llm.llm_extractor_exceptions`, but aren't yet re-exported from the package root — import them directly from that module if you need to catch them.

---

## Known limitations (current state)

This project is workable but still rough around the edges:

- **No automated test suite yet.** `tests/test_init.py` is a live, manual script that makes a real network and LLM call when run — it's useful for manual smoke-testing, but there's no `pytest` setup or `pytest` dev dependency yet. Writing a proper `pytest` suite (unit tests with mocked HTTP/LLM calls) is next on the roadmap.
- **`examples/basic_usage.py` is empty.** Use the [Quick start](#quick-start) and [Usage](#usage) sections above instead.
- **`llm/config.py` is partially unused.** `ModelSpec` and the `resolve_model()`/`build_kwargs()` stubs exist for a future model-fallback/config system, but the current call path in `llm/engine.py` uses `model`/`api_key` directly rather than going through them.
- **The FastAPI app under `api/` has no real endpoints** — just health checks.
- **Only Gemini models have been exercised in practice** so far, even though `model` accepts any `litellm`-supported provider string in principle.

---

## License

MIT — see [LICENSE](LICENSE) for details.