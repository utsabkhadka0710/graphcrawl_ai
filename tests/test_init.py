from graphcrawl_ai.crawl import crawl_url
import json

x = crawl_url(source="https://github.com/utsabkhadka0710",quick_option="summary")

print(json.dumps(x, indent=4))