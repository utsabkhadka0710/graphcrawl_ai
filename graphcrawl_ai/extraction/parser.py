import re
from bs4 import BeautifulSoup

def extract_text_from_html(html_content: str) -> str:
    """
    Clean text parser from raw HTML

    remove unwanted noise from the HTML like nav, link, footer, style, script, etc
    parse the expected nois removed HTML into text
    cleans the text by removing unwanted spaces and lines
    returns the final proper clean text
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
        
    clean_text = soup.get_text(separator=" ", strip=True)
    normalized_text = re.sub(r"\s{2,}",' ',clean_text)

    return normalized_text

        


    