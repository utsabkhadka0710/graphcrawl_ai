import re
from bs4 import BeautifulSoup
from graphcrawl_ai.models.response_models.crawl_url_models.response_url_internal import HtmlParsedContent

def extract_content_from_html(html_content: str) -> HtmlParsedContent:
    """
    Clean text parser from raw HTML

    remove unwanted noise from the HTML like nav, link, footer, style, script, etc
    parse the expected nois removed HTML into text
    cleans the text by removing unwanted spaces and lines
    returns custom data model ScrapedPage which contains the 
     - Document type 
    """

    noise_tags = [
            "meta",
            "script",
            "style",
            "link",
            "iframe",
            "noscript",
            "nav",
            "svg",
            "aside",
            "header",
            "footer",
            ".hidden",
            "[aria-hidden='true']"
        ]
    

    soup = BeautifulSoup(html_content, 'lxml')

    for tag in soup.select(','.join(noise_tags)):
        tag.decompose()
    
    title = soup.title.string if soup.title else "Title Not Found"
    clean_text = soup.get_text(separator=" ", strip=True)
    normalized_text = re.sub(r"\s{2,}",' ',clean_text)

    parsed_content = HtmlParsedContent(
        title = title,
        content = normalized_text
    )

    return parsed_content
