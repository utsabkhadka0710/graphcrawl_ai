import pytest
import lxml
from bs4 import BeautifulSoup
from graphcrawl_ai.extraction.text_from_html import (
    clean_structural_noise,
    clean_semantic_noise,
    extract_content_from_html
)

@pytest.mark.parametrize(
    "html_input, removed_text",
    [
    ("<div><script>alert(1)</script><p>Keep</p></div>", "alert(1)"),
    ("<div style='display: none;'>Hidden Text</div><p>Keep</p>", "Hidden Text"),
    ("<div aria-hidden='true'>Screen reader hide</div><p>Keep</p>", "Screen reader hide"),
    ("<svg><path/></svg><p>Keep</p>", "<svg>")
    ],
    ids = ["script-removed", "style-removed","aria-hidden-removed", "path-removed"]
)
def test_clean_structural_noise(html_input, removed_text):
    """Verify that backend logic blocks, stylesheets, accessibility hide flags, and code assets are dropped."""
    soup = BeautifulSoup(html_input, "lxml")
    cleaned_soup = clean_structural_noise(soup=soup)
    text = cleaned_soup.get_text()
    
    assert removed_text not in text
    assert "Keep" in text
    
def test_clean_semantic_noise_removes_link_heavy_footers():
    """Verify that structural footer blocks with heavy link densities are safely stripped out."""
    html = """
    <div>
        <main>This is the actual good article content that we want to keep.</main>
        <footer class='site-footer'>
            <a href='/1'>Link One</a> <a href='/2'>Link Two</a> 
            <a href='/3'>Link Three</a> <a href='/4'>Link Four</a>
        </footer>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    cleaned_soup = clean_semantic_noise(soup=soup)
    text = cleaned_soup.get_text()
    
    for a in ["Link One","Link Two","Link Three","Link Four"]:
        assert a not in text
    assert "This is the actual good article content that we want to keep." in text
    
def test_clean_semantic_noise_keeps_good_long_content():
    """Verify that comprehensive content blocks are protected by the safety threshold from being deleted."""
    long_text = "This is a very long body text section that spans many lines to pass the 600 character threshold. " * 8
    html = f"<div>{long_text}</div>"
    soup = BeautifulSoup(html, "lxml")
    cleaned_soup = clean_semantic_noise(soup=soup)
    text = cleaned_soup.get_text()
    
    assert len(text)>600
    
def test_extract_content_from_html_integration():
    """Run an integration test confirming that structural, overlay, and link-density cleaners run perfectly in sequence."""
    raw_html = """
    <html>
        <head><style>body {color: red;}</style></head>
        <body>
            <div id="cookie-banner">Accept cookies please</div>
            <nav><a href="/home">Home</a> <a href="/about">About</a></nav>
            <main>
                <h1>AI Scraper Breakthrough</h1>
                <p>The parser successfully extracted this core sentence.</p>
                <div style="display:none">Ignore this hidden tracker text</div>
            </main>
        </body>
    </html>
    """
    result = extract_content_from_html(raw_html)
    
    assert "AI Scraper Breakthrough" in result
    assert "The parser successfully extracted this core sentence." in result
    assert "Accept cookies please" not in result
    assert "Ignore this hidden tracker text" not in result
    assert "Home" not in result


@pytest.mark.parametrize(
    "overlay_snippet, expected_removed_text",
    [
        ("<div id='gdpr-cookie-consent-banner-2026'>We value your privacy</div>", "privacy"),
        ("<aside class='newsletter-box-wrapper'>Subscribe to our feed!</aside>", "Subscribe"),
        ("<section class='promo-discount-wrapper'>Get 20% off now</section>", "20%"),
        ("<div id='popup-modal'>Sign up today</div>", "Sign up"),
        ("<div role='dialog'>Are you sure you want to log out?</div>", "log out"),
        ("<div role='alertdialog'>Warning: Session expiring</div>", "Warning"),
    ],
    ids = ["cookie-removed","newsletter-removed","promo-discount-removed",
           "pop-up-removed","dialog-removed","alert-dialog-removed"]
)
def test_overlay_cleanup_success(overlay_snippet, expected_removed_text):
    """Verify that interstitial popups, marketing promos, and regulatory bars are stripped out."""
    html = f"<html><body>{overlay_snippet}<main><p>Keep this valuable core text.</p></main></body></html>"
    result = extract_content_from_html(html)
    
    assert "Keep this valuable core text." in result
    assert expected_removed_text not in result