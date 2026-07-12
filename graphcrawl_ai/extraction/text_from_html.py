# Keyword-based overlay detection: catches known consent management vendors
# (OneTrust, Cookiebot, etc.) by class/id naming patterns.
# Known limitation: plain-prose cookie notices with no identifying class/id
# are not caught by this approach. This is acceptable for the current bs4-based
# MVP. The Playwright migration will handle dismissal at the browser level,
# making this function obsolete.

import re
from bs4 import BeautifulSoup

def clean_structural_noise(soup: BeautifulSoup)->BeautifulSoup:
    """Strip out elements that define page design, scripts, or are hidden from sight.

    This function hunts down tracking pixels, style blocks, interactive canvases, 
    and elements explicitly marked hidden by screen readers or CSS invisibilities, 
    shredding them completely from the document.
    """
    structural_noise_tags = [
        "style", "script", "noscript",
        "iframe", "svg", "canvas", "dialog"
    ]
    
    for tag in soup.find_all(structural_noise_tags):
        tag.decompose()
    for tag in soup.find_all(attrs={'aria-hidden':'true'}):
        tag.decompose()
    
    invisible_tags =  soup.find_all(
        lambda tag: tag.has_attr('style') and (
            "display:none" in tag['style'].replace(' ','').lower() or 
            "visibility:hidden" in tag['style'].replace(' ','').lower()
            )
        )
    for tag in invisible_tags:
        tag.decompose()
    return soup

def clean_overlay_noise(soup: BeautifulSoup)->BeautifulSoup:
    """Target and remove non-content popups like cookie consent forms and marketing banners.

    This function isolates elements based on accessibility dialog roles or common 
    naming keywords (like 'modal', 'gdpr', or 'subscribe') embedded inside tag IDs 
    and class names, shredding promotional and legal hurdles before text extraction.
    """
    overlay_aria_roles = [
        "dialog", "alertdialog", "banner",
        "navigation", "button", "alert"
    ]
    overlay_keywords = re.compile(
        r'(cookie|consent|privacy-policy|gdpr|modal|popup|overlay|onetrust|osano'
        r'newsletter|subscribe|signup-form|promo|discount-wrapper|newsletter-box)',
        re.IGNORECASE
    )
    
    for role in overlay_aria_roles:
        for tag in soup.find_all(attrs={"role": role}):
            tag.decompose()
    
    for container in soup.find_all(["div", "aside", "section"]):
        container_id = container.get('id','')
        container_class = "".join(container.get('class',[])) if container.get('class') else ""
        
        if (overlay_keywords.search(container_id)) or (overlay_keywords.search(container_class)):
            container.decompose()
            
    return soup
    

def clean_semantic_noise(soup: BeautifulSoup)->BeautifulSoup:
    """Convert an entire raw HTML webpage string into isolated, highly relevant body text.

    This coordinator initializes the processor, executes a multi-stage layout 
    cleanup to drop code structures and hyperlink text maps, gathers the surviving 
    text strings, and unifies layout spaces.
    """
    possible_containers = soup.find_all(['div','aside','section','nav','footer','ul'])
    
    for container in reversed(possible_containers):
    
        if not container.parent:
            continue
        
        total_text = container.get_text(strip=True)
        total_text_len = len(total_text)
        
        if total_text_len == 0:
            container.decompose()
            continue
        
        link_text = "".join([a.get_text(strip=True) for a in container.find_all('a')])
        link_text_len = len(link_text)
        
        link_density = link_text_len/total_text_len
        
        if total_text_len > 600 and link_density < 0.75:
            continue
        
        useful_containers = soup.find_all(['p', 'h2', 'h3', 'h4'])
        if len(useful_containers)>4 and link_density < 0.7:
            continue
        
        if container.name in ["nav", "aside"] and link_density > 0.5:
            container.decompose()
            continue
        
        if link_density > 0.5 and total_text_len < 500:
            container.decompose()
            
    return soup

    
def extract_content_from_html(html_content: str) -> str:
    """Convert an entire raw HTML webpage string into isolated, highly relevant body text.

    This coordinator initializes the processor, executes a multi-stage layout 
    cleanup to drop code structures and hyperlink text maps, gathers the surviving 
    text strings, and unifies layout spaces.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    clean_structural_noise(soup=soup)
    clean_overlay_noise(soup=soup)
    clean_semantic_noise(soup=soup)
    
    text = soup.get_text(separator=" ", strip=True)
    
    clean_text = re.sub(r"\s+"," ",text)
    return clean_text
