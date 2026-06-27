import re
from bs4 import BeautifulSoup
from graphcrawl_ai.models.crawl_url.response_models.parser_response import HtmlParsedContent

def extract_content_from_html(html_content: str) -> HtmlParsedContent:
    """Strip out layout mess and turn raw HTML into clean, readable text.

    This function removes background noise elements (such as navigation menus, 
    scripts, and page styles) from the webpage code and trims down messy spacing 
    to leave behind only the actual written text.

    Args:
        html_content: The raw HTML text code downloaded from a website.

    Returns:
        An HtmlParsedContent object containing the clean page title and 
        the final stripped-down text content.

    Note:
        The parser uses 'lxml' for high-speed processing and applies an 
        automatic cleanup list to eliminate background webpage clutter.
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
