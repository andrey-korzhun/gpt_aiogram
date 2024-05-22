import os
import httpx

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv('OPENAITOKEN'),
                     http_client=httpx.AsyncClient(
                         proxies=os.getenv('PROXYURL'),
                         transport=httpx.HTTPTransport(local_address='0.0.0.0')
                     ))


async def gpt_text(req):
    completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": req}
        ],
        model=os.getenv('CHATGPT_MODEL'),
    )
    return completion
