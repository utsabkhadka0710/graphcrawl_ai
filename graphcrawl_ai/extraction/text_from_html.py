import re
from bs4 import BeautifulSoup
from graphcrawl_ai.models.crawl_url.response_models.parser_response import HtmlParsedContent

def extract_content_from_html(html_content: str) -> HtmlParsedContent:
    """Parse and sanitize raw HTML into structured text.

    This function removes non-content elements (such as navigation, scripts, 
    and metadata) from the provided HTML and normalizes the remaining whitespace.

    Args:
        html_content: The raw HTML string retrieved from a web source.

    Returns:
        An HtmlParsedContent object containing the page title and the 
        sanitized text body.

    Note:
        The parser utilizes 'lxml' for high-performance parsing and applies 
        a whitelist-based removal strategy for noise tags.
    """
    
    noise_tags = [
            "meta", "script", "style", "link",
            "iframe", "noscript", "nav", "svg",
            "aside", "header", "footer", ".hidden",
            "[aria-hidden='true']"
        ]
    

    soup = BeautifulSoup(html_content, 'lxml')

    for tag in soup.select(','.join(noise_tags)):
        tag.decompose()
    
    title = soup.title.string if soup.title else "Title Not Found"
    clean_text = soup.get_text(separator=" ", strip=True)
    normalized_text = re.sub(r"\s+",' ',clean_text)

    parsed_content = HtmlParsedContent(
        title = title,
        content = normalized_text
    )

    return parsed_content
