import os, json
from dotenv import load_dotenv
from google import genai
from graphcrawl_ai.models.request_models.crawl_url_models.request_url_internal import ExtractionRequestToLLM

load_dotenv()

llm_api = str(os.getenv("GEMINI_API"))

def get_response_gemini(request: ExtractionRequestToLLM) -> dict:
    client = genai.Client(api_key=llm_api)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"{request.model_dump()}",
        config={
            'response_mime_type': 'application/json'
        }
    )

    text_response = response.text.encode()
    json_response = json.loads(text_response)

    return json_response