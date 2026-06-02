# GraphCrawl AI 🕷️🕸️

> AI-powered web scraping and structured data extraction — currently under active development.

⚠️ **This project is not ready for use yet.** The API and architecture are still being built and will change significantly.

---

## What is it?

GraphCrawl AI is a Python library for scraping web pages and extracting structured data using AI. Think of it as a developer-friendly pipeline that takes a URL and gives you back clean, structured information — without the usual mess.

---

## Project Structure

```
graphcrawl_ai/
├── graphcrawl_ai/
│   ├── __init__.py
│   ├── crawl.py
│   ├── crawler/
│   ├── extraction/
│   ├── llm/
│   ├── models/
│   └── utils/
├── api/
│   ├── __init__.py
│   ├── crawl.py
│   ├── main.py
│   └── routes/
├── test/
├── examples/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## Status

### 🚧 **Usable GraphCrawl AI - MVP/v.0.1.0 available.**

- Still Improving. Not available on PyPI yet.

#### **But you can try with cloning graphcrawl_ai repository.**

- **Make sure you have Python 3.11+**

- **clone graphcrawrl_ai repository**

- **and test/try out graphcrawl_ai**

**1. Clone the repository**

```bash
git clone https://github.com/utsabkhadka0710/graphcrawl_ai.git
cd graphcrawl_ai
```

**2. Create a test.py graphcrawl_ai**

- `graphcrawl_ai/test.py`

```Python
#leave it empty for now
```

**3. Initialize the virtual environmet**

```bash
python3 -m venv .venv
```

**4. Activate the virtual environment**

- MacOS/Linux
  ```bash
  source .venv/bin/activate
  ```
- Windows
  ```cmd
  .venv\Scripts\activate
  ```

**5. Install editable graphcrawl_ai**

```bash
pip install -e .
```

**6. Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your Gemini API `**no white spaces & no quotation.**` Currently Gemini only avaiable more LLM providers options will be added in the future have some patience.

```.env
GEMINI_API=************************
```

**7. Test GraphCrawl AI with following script or write your own.**

- `graphcrawl*ai/test.py*`

```Python
from graphcrawl_ai.crawl import crawl_url
import json

url = "https://example.com"
prompt = "Enter your prompt here & make sure you ask LLM to strictly response in JSON only or the crawl_ai() may fail."

# For testing I'd suggest you to just go available with quick options

# Here I'm testing with quick otion "auto" which LLM decides itself what's best to crawl
# Available quick options: "summary", "contacts", "products", "auto" try it and experiment yourself
response = crawl_url(source=url, prompt=None, quick_option="auto")
print(json.dumps(response, indent=4))

#I'll add another example below for product(use it for crawling/scraping from e-commerce sites)
url = "https://www.amazon.com/s?k=gaming+headphone"
response = crawl_url(source=url, quick_option="products")
print(json.dumps(response, indent=4))
```

**7. Run test.py**

```bash
python3 test.py
```

## OUTPUT

- If you followed exact steps from above you'll get output without a problem. If you got any please try again still not working raise an issue or contact me: `utsabkhadka9475@gmail.com`

```JSON
{
    "status": "success",
    "page_type": "documentation/placeholder",
    "insights": {
        "title": "Example Domain",
        "core_data": {
            "purpose": "Documentation and example usage",
            "usage_guidelines": "Do not use in actual operations"
        },
        "metadata": {
            "description": "Domain reserved for illustrative purposes in documentation"
        }
    }
}
```

- This is output for crawing/scraping "https://example.com" with "auto" as quick_option.

---

## Feature: AI-powered URL crawling MVP

Implemented the first end-to-end GraphCrawl AI extraction pipeline.

### Current flow:

1. Accept user crawl request
2. Fetch raw HTML from source URL
3. Parse and clean page content
4. Resolve extraction prompt from user prompt or quick option
5. Send extraction request to Gemini
6. Return structured JSON response

### Supported quick extraction modes:

- summary
- contacts
- products
- auto

### This establishes the foundation for future work including:

- provider abstraction
- response validation
- retries
- schema-driven extraction
- async execution
- API endpoints
- browser automation
- document support
- distributed execution

## Planned Features

- Async HTTP fetching
- AI-powered structured extraction
- Browser automation for JavaScript-heavy pages
- Schema-based output validation
- REST API interface
- Background job processing
- GUI for no-code scraping

---

## License

MIT
