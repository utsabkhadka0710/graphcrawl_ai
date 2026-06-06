from graphcrawl_ai.llm import prompts
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_user import ExtractionRequestByUser, QuickOption
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_internal import ExtractionRequestToLLM
from graphcrawl_ai.crawler.fetcher import fetch_html
from graphcrawl_ai.extraction.parser import extract_content_from_html


def resolve_prompt(request: ExtractionRequestByUser) -> ExtractionRequestToLLM:
    source = request.source
    prompt = request.prompt
    quick_option = request.quick_option #request.quick_option hold an enum which is converted to str

    raw_html = fetch_html(url=source)
    clean_content = extract_content_from_html(html_content=raw_html).content

    if not prompt and not quick_option:
        raise ValueError("Prompt missing in the incomming request, request() must have either a prompt or an provided quick option.")
    
    if quick_option and not prompt:
        match quick_option:
            case QuickOption.SUMMARY:
                prompt = prompts.summary
            case QuickOption.CONTACTS:
                prompt = prompts.contacts
            case QuickOption.PRODUCTS:
                prompt = prompts.products
            case QuickOption.AUTO:
                prompt = prompts.auto

    if prompt:
        wrapped_prompt_from_user_prompt = f"""
You are a precise web-scraping AI. Your task is to extract data from a web page based on the User Request.

CRITICAL INSTRUCTION: You must return your response matching this exact JSON schema:
{{
    "status": "success" or "failure",
    "response": [{ "... your extracted data goes here ... "}]
}}

User Request: "{prompt}"

Based on the User Request, determine what fields need to be extracted, extract them from the provided context, and nest them entirely inside the "response" key. Do not add any markdown formatting (like ```json) outside the raw JSON string.
"""

    request_to_llm = ExtractionRequestToLLM(
        content = clean_content,
        prompt = prompt
    )


    return request_to_llm