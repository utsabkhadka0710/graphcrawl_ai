# GraphCrawl AI 🕷️🕸️

> AI-powered web scraping and structured data extraction — currently under active development.

⚠️ **This project is not ready for use yet.** The API and architecture are still being built and will change significantly.

---

## What is it?

GraphCrawl AI is a Python library for scraping web pages and extracting structured data using AI. Think of it as a developer-friendly pipeline that takes a URL and gives you back clean, structured information — without the usual mess.

---

## Project Structure

```
graphcrawl_ai/
├── graphcrawl_ai/
│   ├── __init__.py
│   ├── crawl.py
│   ├── crawler/
│   ├── extraction/
│   ├── llm/
│   ├── models/
│   └── utils/
├── api/
│   ├── __init__.py
│   ├── crawl.py
│   ├── main.py
│   └── routes/
├── test/
├── examples/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## Status

### 🚧 **Usable GraphCrawl AI - MVP/v.0.1.0 available.**

- Still Improving. Not available on PyPI yet.

#### **But you can try with cloning graphcrawl_ai repository.**

- **Make sure you have Python 3.11+**

- **clone graphcrawrl_ai repository**

- **and test/try out graphcrawl_ai**

**1. Clone the repository**

```bash
git clone https://github.com/utsabkhadka0710/graphcrawl_ai.git
cd graphcrawl_ai
```

**2. Create a test.py graphcrawl_ai**

- `graphcrawl_ai/test.py`

```Python
#leave it empty for now
```

**3. Initialize the virtual environmet**

```bash
python3 -m venv .venv
```

**4. Activate the virtual environment**

- MacOS/Linux
  ```bash
  source .venv/bin/activate
  ```
- Windows
  ```cmd
  .venv\Scripts\activate
  ```

**5. Install editable graphcrawl_ai**

```bash
pip install -e .
```

**6. Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your Gemini API `**no white spaces & no quotation.**` Currently Gemini only avaiable more LLM providers options will be added in the future have some patience.

```.env
GEMINI_API=************************
```

**7. Test GraphCrawl AI with following script or write your own.**

- `graphcrawl*ai/test.py*`

```Python
from graphcrawl_ai.crawl import crawl_url
import json

url = "https://example.com"
prompt = "Enter your prompt here & make sure you ask LLM to strictly response in JSON only or the crawl_ai() may fail."

# For testing I'd suggest you to just go available with quick options

# Here I'm testing with quick otion "auto" which LLM decides itself what's best to crawl
# Available quick options: "summary", "contacts", "products", "auto" try it and experiment yourself
response = crawl_url(source=url, prompt=None, quick_option="auto")
print(json.dumps(response, indent=4))

#I'll add another example below for product(use it for crawling/scraping from e-commerce sites)
url = "https://www.amazon.com/s?k=gaming+headphone"
response = crawl_url(source=url, quick_option="products")
print(json.dumps(response, indent=4))
```

**7. Run test.py**

```bash
python3 test.py
```

## OUTPUT

- If you followed exact steps from above you'll get output without a problem. If you got any please try again still not working raise an issue or contact me: `utsabkhadka9475@gmail.com`

```JSON
| 2026-06-02 21:44:33,696 | INFO | Attempt to fetch HTML from 'https://example.com'. | Attempt = 1 |
| 2026-06-02 21:44:33,831 | INFO | HTTP Request: GET https://example.com "HTTP/1.1 200 OK" |
| 2026-06-02 21:44:33,833 | INFO | HTML/Data Fetched Successfully. |
| 2026-06-02 21:44:33,853 | INFO | AFC is enabled with max remote calls: 10. |
| 2026-06-02 21:44:35,420 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/... "HTTP/1.1 200 OK" |
{
    "status": "success",
    "page_type": "documentation/placeholder",
    "insights": {
        "title": "Example Domain",
        "core_data": {
            "purpose": "Documentation and illustrative examples",
            "usage_guidance": "Do not use in operations",
            "accessibility": "Publicly available for non-operational use"
        },
        "metadata": {
            "domain_status": "reserved"
        }
    }
}
| 2026-06-02 21:44:35,423 | INFO | Attempt to fetch HTML from 'https://www.amazon.com/s?k=gaming+headphone'. | Attempt = 1 |
| 2026-06-02 21:44:36,035 | INFO | HTTP Request: GET https://www.amazon.com/s?k=gaming+headphone "HTTP/1.1 200 OK" |
| 2026-06-02 21:44:36,759 | INFO | HTML/Data Fetched Successfully. |
| 2026-06-02 21:44:36,892 | INFO | AFC is enabled with max remote calls: 10. |
| 2026-06-02 21:44:42,589 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/... "HTTP/1.1 200 OK" |
{
    "status": "success",
    "products_found": true,
    "products": [
        {
            "name": "HyperX Cloud Stinger 2 Core \u2013 PC Gaming Headset",
            "price": "$30.64",
            "description": "Lightweight Over-Ear Headset with mic, Swivel-to-Mute mic Function, DTS Headphone:X Spatial Audio, 40mm Drivers,Black",
            "rating": "Not provided",
            "total_sold": "100+ bought in past month",
            "other_info": {
                "buying_options": "2 used & new offers"
            }
        },
        {
            "name": "Razer BlackShark V2 X PlayStation Gaming Headset",
            "price": "$26.99",
            "description": "50mm Drivers - Cardioid Mic - Lightweight - Comfortable, Noise Isolating Earcups - for PS5, Xbox Series X, PC, Switch via 3.5 mm Audio Jack - Black",
            "rating": "Not provided",
            "total_sold": "1K+ bought in past month",
            "other_info": {
                "buying_options": "22 used & new offers"
            }
        },
        {
            "name": "Logitech G PRO X Wireless Lightspeed Gaming Headset",
            "price": "$135.00",
            "description": "Blue VO!CE Mic Filter Tech, 50 mm PRO-G Drivers, and DTS Headphone:X 2.0 Surround Sound, 20+ Hour Battery Life - Black",
            "rating": "Not provided",
            "total_sold": "300+ bought in past month",
            "other_info": {
                "buying_options": "4 used & new offers"
            }
        },
        {
            "name": "SteelSeries Arctis Nova 1P Multi-System Gaming Headset",
            "price": "$45.67",
            "description": "Hi-Fi Drivers \u2014 360\u00b0 Spatial Audio \u2014 Comfort Design \u2014 Durable \u2014 Lightweight \u2014 Noise-Cancelling Mic \u2014 PS5/PS4, PC, Xbox, Switch - White",
            "rating": "Not provided",
            "total_sold": "200+ bought in past month",
            "other_info": {
                "buying_options": "12 used & new offers"
            }
        },
        {
            "name": "ASUS ROG Kithara Gaming/Audiophile Open-Back Wired Headphones",
            "price": "$255.62",
            "description": "ROG-Tuned HIFIMAN Planar Magnetic Drivers, Adjustable Headband, Extra Ear Pads, Compatible with DACs, Amps, PC, Console, Mobile",
            "rating": "Not provided",
            "total_sold": "100+ bought in past month",
            "other_info": {
                "buying_options": "25 used & new offers"
            }
        },
        {
            "name": "SteelSeries Arctis Nova Pro Multi-System Gaming Headset",
            "price": "$176.08",
            "description": "Premium Hi-Fi Drivers, Hi-Res Audio - 360\u00b0 Spatial Audio - GameDAC Gen 2 - ESS Sabre Quad-DAC - Stealth Retractable Mic - PC, PS5, PS4, Switch",
            "rating": "Not provided",
            "total_sold": "100+ bought in past month",
            "other_info": {
                "buying_options": "18 used & new offers",
                "sustainability": "Energy efficiency, Safer chemicals, Manufacturing practices, Worker well-being"
            }
        },
        {
            "name": "Sony INZONE H5 Wireless Gaming Headset",
            "price": "$115.00",
            "description": "360 Spatial Sound, Works with PC, PS5, 28 Hour Battery, 2.4Ghz Wireless and 3.5mm Audio Jack, WH-G500 Black",
            "rating": "Not provided",
            "total_sold": "Not provided",
            "other_info": {
                "buying_options": "9 used & new offers"
            }
        },
        {
            "name": "Sony INZONE H3 Wired Gaming Headphones With Mic",
            "price": "$61.83",
            "description": "PS5 Headphones, Over-Ear, Personalized 360 Spatial Sound, Discord Certified MDR-G300 (White)",
            "rating": "Not provided",
            "total_sold": "Not provided",
            "other_info": {
                "buying_options": "5 used & new offers"
            }
        },
        {
            "name": "Sony MDR7506 Professional Large Diaphragm Headphone",
            "price": "$92.30",
            "description": "Top Reviewed for Sound quality",
            "rating": "Top Reviewed",
            "total_sold": "2K+ bought in past month",
            "other_info": {
                "buying_options": "8 used & new offers"
            }
        },
        {
            "name": "Corsair Void v2 Wireless Gaming Headset",
            "price": "$81.76",
            "description": "With Bluetooth for PC, PS5, PS4, Switch, Mobile \u2013 Dolby Atmos, 70 Hr Battery, Dual Wireless, Lightweight, Fast Charging \u2013 Carbon",
            "rating": "Not provided",
            "total_sold": "500+ bought in past month",
            "other_info": {
                "buying_options": "21 used & new offers"
            }
        },
        {
            "name": "Sony WH-1000XM6 The Best Noise Canceling Wireless Headphones",
            "price": "$331.80",
            "description": "HD NC Processor QN3, 12 Microphones, Adaptive NC Optimizer, Mastered by Engineers, Studio-Quality, 30-Hour Battery, Black",
            "rating": "Top Reviewed",
            "total_sold": "1K+ bought in past month",
            "other_info": {
                "buying_options": "4 used & new offers"
            }
        },
        {
            "name": "HyperX Cloud III \u2013 Wired Gaming Headset",
            "price": "$75.99",
            "description": "PC, PS5, Xbox Series X|S, Angled 53mm Drivers, DTS, Memory Foam, Durable Frame, Ultra-Clear 10mm Mic, USB-C, USB-A, 3.5mm \u2013 Pink",
            "rating": "Top Reviewed",
            "total_sold": "300+ bought in past month",
            "other_info": {
                "buying_options": "2 used & new offers"
            }
        },
        {
            "name": "Razer Barracuda X Wireless Gaming & Mobile Headset",
            "price": "$65.69",
            "description": "PC, PlayStation, Switch 2, Android, iOS: 2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Mercury White",
            "rating": "Not provided",
            "total_sold": "200+ bought in past month",
            "other_info": {
                "buying_options": "5 used & new offers"
            }
        },
        {
            "name": "Audio-Technica ATH-M50X Professional Studio Monitor Headphones",
            "price": "$141.50",
            "description": "Black, Professional Grade, Critically Acclaimed, with Detachable Cable #1 Top Rated",
            "rating": "#1 Top Rated",
            "total_sold": "1K+ bought in past month",
            "other_info": {
                "buying_options": "34 used & new offers"
            }
        },
        {
            "name": "Logitech G435 Lightspeed and Bluetooth Wireless Gaming Headset (Renewed)",
            "price": "Not provided",
            "description": "Lightweight- Black (Renewed)",
            "rating": "Not provided",
            "total_sold": "100+ bought in past month",
            "other_info": {
                "buying_options": "Not provided"
            }
        },
        {
            "name": "Fachixy Wireless Gaming Headset with Microphone",
            "price": "$33.39",
            "description": "For PC, PS5, PS4, Bluetooth Gaming Headphones - Fast Charge 50Hr Battery, Cool LED Lights for Switch, Laptop, Mobile, Mac 2.4GHz Gamer Headset",
            "rating": "Not provided",
            "total_sold": "Not provided",
            "other_info": {
                "buying_options": "7 new offers"
            }
        }
    ]
}
```

- This is output for crawing/scraping "https://example.com" with "auto" as quick_option. and "https://amazon.com/" with "products" as quick option.

---

## Feature: AI-powered URL crawling MVP

Implemented the first end-to-end GraphCrawl AI extraction pipeline.

### Current flow:

1. Accept user crawl request
2. Fetch raw HTML from source URL
3. Parse and clean page content
4. Resolve extraction prompt from user prompt or quick option
5. Send extraction request to Gemini
6. Return structured JSON response

### Supported quick extraction modes:

- summary
- contacts
- products
- auto

### This establishes the foundation for future work including:

- provider abstraction
- response validation
- retries
- schema-driven extraction
- async execution
- API endpoints
- browser automation
- document support
- distributed execution

## Planned Features

- Async HTTP fetching
- AI-powered structured extraction
- Browser automation for JavaScript-heavy pages
- Schema-based output validation
- REST API interface
- Background job processing
- GUI for no-code scraping

---

## License

MIT
