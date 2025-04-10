from config import CF_API_BASE
from cf_request import make_cf_request

async def get_user_contest(handle : str) -> str :
    url = f"{CF_API_BASE}contest.list?gym=false"
    data = await make_cf_request(url)