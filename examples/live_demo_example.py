from graphcrawl_ai import crawl_url
from dotenv import load_dotenv

load_dotenv()

url = "https://www.amazon.com/s?k=gaming+headphone"
prompt = "Extract a detail imformation about this user with thh cotacts if any"

# For testing I'd suggest  you to just go with quick option available

# Here I'm testing with quick otion "auto" which LLM decides itself what's best to crawl
# Available quick options: "summary", "contacts", "products", "auto" try it and experiment yourself
response = crawl_url(
    source=url,
    quick_option='products',
    model="gemini/gemini-2.5-flash"
    )

print(response)
print(response.model_dump())
print(response.model_dump_json(indent=4))
print(type(response))