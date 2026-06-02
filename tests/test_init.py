from graphcrawl_ai.crawl import crawl_url
import json

url = "https://example.com"
prompt = "Enter your prompt here"

# For testing I'd suggest  you to just go with quick option available

# Here I'm testing with quick otion "auto" which LLM decides itself what's best to crawl
# Available quick options: "summary", "contacts", "products", "auto" try it and experiment yourself
response = crawl_url(source=url, prompt=None, quick_option="auto")
print(json.dumps(response, indent=4))

# I'll add another example below for product(use it for crawling/scraping from e-commerce sites)
url = "https://www.amazon.com/s?k=gaming+headphone"
response = crawl_url(source=url, quick_option="products")
print(json.dumps(response, indent=4))