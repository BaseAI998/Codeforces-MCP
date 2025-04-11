from typing import Any
import httpx
from config import USER_AGENT

async def make_cf_request(url : str) -> dict[str, Any] | str :
    headers = {
        "User-Agent" : USER_AGENT,
        "Accept" : "application/json"
    }
    async with httpx.AsyncClient() as client :
        try :
            response = await client.get(url=url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e :
            return str(e)