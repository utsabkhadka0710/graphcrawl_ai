from graphcrawl_ai.llm import prompts
from graphcrawl_ai.models.request import ExtractionRequestByUser, ExtractionRequestToLLM, QuickOption
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


    request_to_llm = ExtractionRequestToLLM(
        content = clean_content,
        prompt = prompt
    )


    return request_to_llm