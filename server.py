from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("codeforces-MCP")

CF_API_BASE = "https://codeforces.com/api/"
USER_AGENT = "MCP-Codeforces/1.0 (Python; httpx)"

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
        
@mcp.tool()
async def get_user_rating(handle : str) -> str :
    url = f"{CF_API_BASE}user.rating?handle={handle}"
    data = await make_cf_request(url)
    if type(data) == str :
        return data        
    if "result" in data:
        ratings = [f"rating : {rating['newRating']}" for rating in data['result']]
        return "\n---\n".join(ratings)
    else :
        return "rusult不在data中"
    return str(data)

if __name__ == "__main__" :
    mcp.run(transport='stdio')