import lxml
from bs4 import BeautifulSoup

def clean_structural_noise(soup: BeautifulSoup)->BeautifulSoup:
    structural_noise_tags = [
        "style", "script", "noscript",
        "iframe", "svg", "canvas", 
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

def clean_semantic_noise(soup: BeautifulSoup)->BeautifulSoup:
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
        
        if link_density > 0.5:
            container.decompose()
            
    return soup
    
def extract_content_from_html(html_content: str) -> str:
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    clean_structural_noise(soup=soup)
    clean_semantic_noise(soup=soup)
    
    text = soup.get_text(separator=" ", strip=True)
    
    from re import sub
    clean_text = sub(r"\s+"," ",text)
    
    return clean_text

    