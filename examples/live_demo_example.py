import asyncio
from graphcrawl_ai import crawl_url
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
load_dotenv()

url = "https://github.com/utsabkhadka0710/"
prompt = "Extract detailed information about the user"

class UserInfo(BaseModel):
    name: str
    age: Optional[int]
    contact_info: list[str]
    summary: str
    
class Schema(BaseModel):
    info: UserInfo

response = asyncio.run(crawl_url(
    source=url,
    prompt=prompt,
    response_schema=Schema,
    model="gemini/gemini-3.1-flash-lite"
))

print(response)
print(response.model_dump())
print(response.model_dump_json(indent=4))
print(type(response))