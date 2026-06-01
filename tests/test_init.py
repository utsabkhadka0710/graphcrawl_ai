from graphcrawl_ai.extraction.extraction_request import request

x = request(source="https://github.com/utsabkhadka0710",quick_option="products")

print(x.get('quick_option'))