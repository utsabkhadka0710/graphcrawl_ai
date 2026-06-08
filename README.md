# GraphCrawl AI 🕷️🕸️

> AI-powered web scraping and structured data extraction — currently under active development.

⚠️ **This project is not ready for use yet.** The API and architecture are still being built and will change significantly.

---

## What is it?

GraphCrawl AI is a Python library that turns any public webpage into structured, typed data using AI. You point it at a URL, tell it what you want (or let it decide), and get back a clean Pydantic model — no HTML parsing boilerplate, no prompt engineering required.

---

## How it works

```
URL → HTTP fetch → HTML cleaning → Gemini LLM → Pydantic response object
```

1. **Fetcher** — downloads the raw HTML with retry and timeout logic (`httpx`)
2. **Parser** — strips noise tags (scripts, nav, footer, ads) and normalizes whitespace (`beautifulsoup4` + `lxml`)
3. **Request resolver** — picks the right prompt and response schema based on your chosen mode
4. **Gemini extractor** — sends the clean text to Gemini and parses the JSON response back into a typed Pydantic model

---

## Requirements

- Python ≥ 3.11
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## Installation

install from source:

```bash
git clone https://github.com/your-username/graphcrawl_ai.git
cd graphcrawl_ai
pip install -e .
```

---

## Configuration

Create a `.env` file in your project root (see `.env.example`):

```env
GEMINI_API=your_gemini_api_key_here
```

The library loads this automatically via `python-dotenv`.

---

## Quick start

```python
from graphcrawl_ai import crawl_url

# Get a summary of any webpage
result = crawl_url(
    source="https://example.com/blog/post",
    quick_option="summary"
)

print(result.summary)
print(result.key_takeaways)
```

---

## Usage

### `crawl_url()`

The single public entry point for the library.

```python
crawl_url(
    source: str,
    prompt: str = None,
    quick_option: Literal["summary", "contacts", "products", "auto"] = None,
    llm_timeout: float = 60,
    llm_retry: int = 3,
    timeout: float = 30,
    retry: int = 3,
    response_schema: type[BaseModel] | None = None
) -> BaseModel
```

You must provide either `prompt` or `quick_option` — not neither, not both(if both are provided GraphCrawl will choose prompt over quick_option).

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
    quick_option="contacts"
)

print(result.contact_info.emails)
print(result.contact_info.phones)
print(result.contact_info.social_links)
```

### Example: extract products

```python
result = crawl_url(
    source="https://shop.example.com/category/headphones",
    quick_option="products"
)

for product in result.products:
    print(product.name, product.price)
```

### Example: custom prompt

```python
result = crawl_url(
    source="https://techblog.example.com/article",
    prompt="Extract the author name, publication date, and all external links mentioned."
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
    timeout=60,       # seconds to wait for the webpage
    retry=5,          # retry attempts for the HTTP fetch
    llm_timeout=120,  # seconds to wait for Gemini
    llm_retry=5,      # retry attempts for the LLM call
)
```

---

## Response models

All responses extend `UrlBaseResponse` which carries a `status` field (`"success"` or `"failure"`). Every response is a valid Pydantic model — call `.model_dump()` for a dict or `.model_dump_json()` for JSON.

```python
result = crawl_url(source="https://example.com", quick_option="summary")

print(result.status)                    # "success"
print(result.model_dump())              # dict
print(result.model_dump_json(indent=2)) # pretty JSON
```

---

## Project structure

```
graphcrawl_ai/
├── graphcrawl_ai/
│   ├── crawl.py                          # Public API: crawl_url()
│   ├── crawler/
│   │   └── fetcher.py                    # HTTP fetch with retry
│   ├── extraction/
│   │   └── parser.py                     # HTML → clean text
│   ├── llm/
│   │   ├── gemini_extractor.py           # Gemini API client
│   │   ├── prompts.py                    # Built-in prompts for quick options
│   │   └── request_resolver/
│   │       └── user_url_request_resolver.py  # Routing logic
│   └── models/
│       ├── request_models/               # Input schemas
│       └── response_models/              # Output schemas
├── api/
│   └── main.py                           # FastAPI app (in progress)
├── examples/
│   └── basic_usage.py
├── tests/
│   └── test_init.py
├── pyproject.toml
└── .env.example
```

---

## REST API

A FastAPI application is included under `api/` and is currently under active development. To run it locally:

```bash
uvicorn api.main:app --reload
```

---

## Error handling

The library raises `FetchError` (from `graphcrawl_ai.crawler.fetcher`) for network-level failures:

```python
from graphcrawl_ai import crawl_url
from graphcrawl_ai.crawler.fetcher import FetchError

try:
    result = crawl_url(source="https://example.com", quick_option="summary")
except FetchError as e:
    print(f"Could not fetch the page: {e}")
except ValueError as e:
    print(f"Bad request: {e}")  # Missing prompt and quick_option
```

---

## License

MIT — see [LICENSE](LICENSE) for details.