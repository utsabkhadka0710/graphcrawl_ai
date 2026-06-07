from graphcrawl_ai.crawl import crawl_url
import json

url = "https://www.amazon.com/s?k=gaming+headphone"
prompt = "Extract a detail imformation about this user with thh cotacts if any"

# For testing I'd suggest  you to just go with quick option available

# Here I'm testing with quick otion "auto" which LLM decides itself what's best to crawl
# Available quick options: "summary", "contacts", "products", "auto" try it and experiment yourself
response = crawl_url(source=url, quick_option='products')

print(response)
print(response.model_dump())
print(response.model_dump_json(indent=4))
print(type(response))

"""
```OUTPUT:
INFO | Attempt to fetch HTML from 'https://www.amazon.com/s?k=gaming+headphone'. | Attempt = 1
INFO | HTTP Request: GET https://www.amazon.com/s?k=gaming+headphone "HTTP/1.1 200 OK"
INFO | HTML/Data Fetched Successfully.
INFO | AFC is enabled with max remote calls: 10.
^AINFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent "HTTP/1.1 200 OK"
status='success' products_found=True products=[ProductItem(name='Razer BlackShark V2 X PlayStation Gaming Headset', price='$27.29', description='50mm Drivers - Cardioid Mic - Lightweight - Comfortable, Noise Isolating Earcups - for PS5, Xbox Series X, PC, Switch via 3.5 mm Audio Jack - Black', rating='Not specified', total_sold='3K+ bought in past month'), ProductItem(name='HyperX Cloud Stinger 2 Core - Gaming Headset for Playstation', price='$18.98', description='Lightweight Over-Ear Headset with mic, Swivel-to-Mute Function, 40mm Drivers - Black', rating='Not specified', total_sold='500+ bought in past month'), ProductItem(name='Logitech G Pro X Wired Gaming Headset', price='$68.81', description='Blue VO!CE Detachable Boom Mic, DTS 7.1, 50 mm Drivers, USB/3.5mm Aux, Spare Memory Foam Ear Pads, USB DAC & Bag Included - Black', rating='Not specified', total_sold='1K+ bought in past month'), ProductItem(name='Sony INZONE H5 Wireless Gaming Headset', price='$115.00', description='360 Spatial Sound, Works with PC, PS5, 28 Hour Battery, 2.4Ghz Wireless and 3.5mm Audio Jack, WH-G500 Black', rating='Not specified', total_sold='100+ bought in past month'), ProductItem(name='ASUS ROG Kithara Gaming/Audiophile Open-Back Wired Headphones with Mic', price='$247.84', description='ROG-Tuned HIFIMAN Planar Magnetic Drivers, Adjustable Headband, Extra Ear Pads, Compatible with DACs, Amps, PC, Console, Mobile', rating='Not specified', total_sold='200+ bought in past month'), ProductItem(name='Sony WH-1000XM6 The Best Noise Canceling Wireless Headphones', price='$331.80', description='HD NC Processor QN3, 12 Microphones, Adaptive NC Optimizer, Mastered by Engineers, Studio-Quality, 30-Hour Battery, Black', rating='Top Reviewed for Sound quality', total_sold='3K+ bought in past month'), ProductItem(name='Sony INZONE H3 Wired Gaming Headphones With Mic', price='$61.83', description='PS5 Headphones, Over-Ear, Personalized 360 Spatial Sound, Discord Certified MDR-G300 (White)', rating='Not specified', total_sold='50+ bought in past month'), ProductItem(name='Razer Barracuda X Wireless Gaming & Mobile Headset (Mercury White)', price='$65.69', description='2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Mercury White', rating='Not specified', total_sold='300+ bought in past month'), ProductItem(name='Corsair Void v2 Wireless Gaming Headset with Bluetooth', price='$81.76', description='for PC, PS5, PS4, Switch, Mobile – Dolby Atmos, 70 Hr Battery, Dual Wireless, Lightweight, Fast Charging – Carbon', rating='Not specified', total_sold='1K+ bought in past month'), ProductItem(name='HyperX Cloud III – Wired Gaming Headset', price='$119.02', description='PC, PS5, Xbox Series X|S, Angled 53mm Drivers, DTS, Memory Foam, Durable Frame, Ultra-Clear 10mm Mic, USB-C, USB-A, 3.5mm – Pink', rating='Top Reviewed for Sound quality', total_sold='600+ bought in past month'), ProductItem(name='Sony MDR7506 Professional Large Diaphragm Headphone', price='$93.03', description='Professional Grade, Large Diaphragm Headphone', rating='Top Reviewed for Sound quality', total_sold='3K+ bought in past month'), ProductItem(name='Audio-Technica ATH-M50X Professional Studio Monitor Headphones', price='$141.50', description='Black, Professional Grade, Critically Acclaimed, with Detachable Cable', rating='#1 Top Rated', total_sold='2K+ bought in past month'), ProductItem(name='SteelSeries Arctis Nova 1 Multi-System Gaming Headset', price='$44.99', description='Hi-Fi Drivers — 360° Spatial Audio — Comfort Design — Durable — Ultra Lightweight — Noise-Cancelling Mic — PC, PS5/PS4, Switch, Xbox - White', rating='Not specified', total_sold='200+ bought in past month'), ProductItem(name='SteelSeries Arctis Nova Pro X Gaming Headset for Xbox', price='$136.95', description='Signature Arctis Sound, Sustainability features certified', rating='Not specified', total_sold='100+ bought in past month'), ProductItem(name='Razer Barracuda X Wireless Gaming & Mobile Headset (Black)', price='$56.14', description='2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Black, Sustainability features certified', rating='Not specified', total_sold='500+ bought in past month'), ProductItem(name='DROP PC38X Gaming Headset', price='$100.24', description='Open-Back Over-Ear Design with Noise-Cancelling Mic, Velour Earpads – Compatible with PC, PS5, PS4, Xbox, Switch, Mobile – Black', rating='Not specified', total_sold='Not specified')]
{'status': 'success', 'products_found': True, 'products': [{'name': 'Razer BlackShark V2 X PlayStation Gaming Headset', 'price': '$27.29', 'description': '50mm Drivers - Cardioid Mic - Lightweight - Comfortable, Noise Isolating Earcups - for PS5, Xbox Series X, PC, Switch via 3.5 mm Audio Jack - Black', 'rating': 'Not specified', 'total_sold': '3K+ bought in past month'}, {'name': 'HyperX Cloud Stinger 2 Core - Gaming Headset for Playstation', 'price': '$18.98', 'description': 'Lightweight Over-Ear Headset with mic, Swivel-to-Mute Function, 40mm Drivers - Black', 'rating': 'Not specified', 'total_sold': '500+ bought in past month'}, {'name': 'Logitech G Pro X Wired Gaming Headset', 'price': '$68.81', 'description': 'Blue VO!CE Detachable Boom Mic, DTS 7.1, 50 mm Drivers, USB/3.5mm Aux, Spare Memory Foam Ear Pads, USB DAC & Bag Included - Black', 'rating': 'Not specified', 'total_sold': '1K+ bought in past month'}, {'name': 'Sony INZONE H5 Wireless Gaming Headset', 'price': '$115.00', 'description': '360 Spatial Sound, Works with PC, PS5, 28 Hour Battery, 2.4Ghz Wireless and 3.5mm Audio Jack, WH-G500 Black', 'rating': 'Not specified', 'total_sold': '100+ bought in past month'}, {'name': 'ASUS ROG Kithara Gaming/Audiophile Open-Back Wired Headphones with Mic', 'price': '$247.84', 'description': 'ROG-Tuned HIFIMAN Planar Magnetic Drivers, Adjustable Headband, Extra Ear Pads, Compatible with DACs, Amps, PC, Console, Mobile', 'rating': 'Not specified', 'total_sold': '200+ bought in past month'}, {'name': 'Sony WH-1000XM6 The Best Noise Canceling Wireless Headphones', 'price': '$331.80', 'description': 'HD NC Processor QN3, 12 Microphones, Adaptive NC Optimizer, Mastered by Engineers, Studio-Quality, 30-Hour Battery, Black', 'rating': 'Top Reviewed for Sound quality', 'total_sold': '3K+ bought in past month'}, {'name': 'Sony INZONE H3 Wired Gaming Headphones With Mic', 'price': '$61.83', 'description': 'PS5 Headphones, Over-Ear, Personalized 360 Spatial Sound, Discord Certified MDR-G300 (White)', 'rating': 'Not specified', 'total_sold': '50+ bought in past month'}, {'name': 'Razer Barracuda X Wireless Gaming & Mobile Headset (Mercury White)', 'price': '$65.69', 'description': '2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Mercury White', 'rating': 'Not specified', 'total_sold': '300+ bought in past month'}, {'name': 'Corsair Void v2 Wireless Gaming Headset with Bluetooth', 'price': '$81.76', 'description': 'for PC, PS5, PS4, Switch, Mobile – Dolby Atmos, 70 Hr Battery, Dual Wireless, Lightweight, Fast Charging – Carbon', 'rating': 'Not specified', 'total_sold': '1K+ bought in past month'}, {'name': 'HyperX Cloud III – Wired Gaming Headset', 'price': '$119.02', 'description': 'PC, PS5, Xbox Series X|S, Angled 53mm Drivers, DTS, Memory Foam, Durable Frame, Ultra-Clear 10mm Mic, USB-C, USB-A, 3.5mm – Pink', 'rating': 'Top Reviewed for Sound quality', 'total_sold': '600+ bought in past month'}, {'name': 'Sony MDR7506 Professional Large Diaphragm Headphone', 'price': '$93.03', 'description': 'Professional Grade, Large Diaphragm Headphone', 'rating': 'Top Reviewed for Sound quality', 'total_sold': '3K+ bought in past month'}, {'name': 'Audio-Technica ATH-M50X Professional Studio Monitor Headphones', 'price': '$141.50', 'description': 'Black, Professional Grade, Critically Acclaimed, with Detachable Cable', 'rating': '#1 Top Rated', 'total_sold': '2K+ bought in past month'}, {'name': 'SteelSeries Arctis Nova 1 Multi-System Gaming Headset', 'price': '$44.99', 'description': 'Hi-Fi Drivers — 360° Spatial Audio — Comfort Design — Durable — Ultra Lightweight — Noise-Cancelling Mic — PC, PS5/PS4, Switch, Xbox - White', 'rating': 'Not specified', 'total_sold': '200+ bought in past month'}, {'name': 'SteelSeries Arctis Nova Pro X Gaming Headset for Xbox', 'price': '$136.95', 'description': 'Signature Arctis Sound, Sustainability features certified', 'rating': 'Not specified', 'total_sold': '100+ bought in past month'}, {'name': 'Razer Barracuda X Wireless Gaming & Mobile Headset (Black)', 'price': '$56.14', 'description': '2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Black, Sustainability features certified', 'rating': 'Not specified', 'total_sold': '500+ bought in past month'}, {'name': 'DROP PC38X Gaming Headset', 'price': '$100.24', 'description': 'Open-Back Over-Ear Design with Noise-Cancelling Mic, Velour Earpads – Compatible with PC, PS5, PS4, Xbox, Switch, Mobile – Black', 'rating': 'Not specified', 'total_sold': 'Not specified'}]}
{
    "status": "success",
    "products_found": true,
    "products": [
        {
            "name": "Razer BlackShark V2 X PlayStation Gaming Headset",
            "price": "$27.29",
            "description": "50mm Drivers - Cardioid Mic - Lightweight - Comfortable, Noise Isolating Earcups - for PS5, Xbox Series X, PC, Switch via 3.5 mm Audio Jack - Black",
            "rating": "Not specified",
            "total_sold": "3K+ bought in past month"
        },
        {
            "name": "HyperX Cloud Stinger 2 Core - Gaming Headset for Playstation",
            "price": "$18.98",
            "description": "Lightweight Over-Ear Headset with mic, Swivel-to-Mute Function, 40mm Drivers - Black",
            "rating": "Not specified",
            "total_sold": "500+ bought in past month"
        },
        {
            "name": "Logitech G Pro X Wired Gaming Headset",
            "price": "$68.81",
            "description": "Blue VO!CE Detachable Boom Mic, DTS 7.1, 50 mm Drivers, USB/3.5mm Aux, Spare Memory Foam Ear Pads, USB DAC & Bag Included - Black",
            "rating": "Not specified",
            "total_sold": "1K+ bought in past month"
        },
        {
            "name": "Sony INZONE H5 Wireless Gaming Headset",
            "price": "$115.00",
            "description": "360 Spatial Sound, Works with PC, PS5, 28 Hour Battery, 2.4Ghz Wireless and 3.5mm Audio Jack, WH-G500 Black",
            "rating": "Not specified",
            "total_sold": "100+ bought in past month"
        },
        {
            "name": "ASUS ROG Kithara Gaming/Audiophile Open-Back Wired Headphones with Mic",
            "price": "$247.84",
            "description": "ROG-Tuned HIFIMAN Planar Magnetic Drivers, Adjustable Headband, Extra Ear Pads, Compatible with DACs, Amps, PC, Console, Mobile",
            "rating": "Not specified",
            "total_sold": "200+ bought in past month"
        },
        {
            "name": "Sony WH-1000XM6 The Best Noise Canceling Wireless Headphones",
            "price": "$331.80",
            "description": "HD NC Processor QN3, 12 Microphones, Adaptive NC Optimizer, Mastered by Engineers, Studio-Quality, 30-Hour Battery, Black",
            "rating": "Top Reviewed for Sound quality",
            "total_sold": "3K+ bought in past month"
        },
        {
            "name": "Sony INZONE H3 Wired Gaming Headphones With Mic",
            "price": "$61.83",
            "description": "PS5 Headphones, Over-Ear, Personalized 360 Spatial Sound, Discord Certified MDR-G300 (White)",
            "rating": "Not specified",
            "total_sold": "50+ bought in past month"
        },
        {
            "name": "Razer Barracuda X Wireless Gaming & Mobile Headset (Mercury White)",
            "price": "$65.69",
            "description": "2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Mercury White",
            "rating": "Not specified",
            "total_sold": "300+ bought in past month"
        },
        {
            "name": "Corsair Void v2 Wireless Gaming Headset with Bluetooth",
            "price": "$81.76",
            "description": "for PC, PS5, PS4, Switch, Mobile – Dolby Atmos, 70 Hr Battery, Dual Wireless, Lightweight, Fast Charging – Carbon",
            "rating": "Not specified",
            "total_sold": "1K+ bought in past month"
        },
        {
            "name": "HyperX Cloud III – Wired Gaming Headset",
            "price": "$119.02",
            "description": "PC, PS5, Xbox Series X|S, Angled 53mm Drivers, DTS, Memory Foam, Durable Frame, Ultra-Clear 10mm Mic, USB-C, USB-A, 3.5mm – Pink",
            "rating": "Top Reviewed for Sound quality",
            "total_sold": "600+ bought in past month"
        },
        {
            "name": "Sony MDR7506 Professional Large Diaphragm Headphone",
            "price": "$93.03",
            "description": "Professional Grade, Large Diaphragm Headphone",
            "rating": "Top Reviewed for Sound quality",
            "total_sold": "3K+ bought in past month"
        },
        {
            "name": "Audio-Technica ATH-M50X Professional Studio Monitor Headphones",
            "price": "$141.50",
            "description": "Black, Professional Grade, Critically Acclaimed, with Detachable Cable",
            "rating": "#1 Top Rated",
            "total_sold": "2K+ bought in past month"
        },
        {
            "name": "SteelSeries Arctis Nova 1 Multi-System Gaming Headset",
            "price": "$44.99",
            "description": "Hi-Fi Drivers — 360° Spatial Audio — Comfort Design — Durable — Ultra Lightweight — Noise-Cancelling Mic — PC, PS5/PS4, Switch, Xbox - White",
            "rating": "Not specified",
            "total_sold": "200+ bought in past month"
        },
        {
            "name": "SteelSeries Arctis Nova Pro X Gaming Headset for Xbox",
            "price": "$136.95",
            "description": "Signature Arctis Sound, Sustainability features certified",
            "rating": "Not specified",
            "total_sold": "100+ bought in past month"
        },
        {
            "name": "Razer Barracuda X Wireless Gaming & Mobile Headset (Black)",
            "price": "$56.14",
            "description": "2.4GHz Wireless + Bluetooth - Lightweight - 40mm Drivers - Detachable Mic - 50 Hr Battery - Black, Sustainability features certified",
            "rating": "Not specified",
            "total_sold": "500+ bought in past month"
        },
        {
            "name": "DROP PC38X Gaming Headset",
            "price": "$100.24",
            "description": "Open-Back Over-Ear Design with Noise-Cancelling Mic, Velour Earpads – Compatible with PC, PS5, PS4, Xbox, Switch, Mobile – Black",
            "rating": "Not specified",
            "total_sold": "Not specified"
        }
    ]
}
<class 'graphcrawl_ai.UrlProductsResponse'>
"""