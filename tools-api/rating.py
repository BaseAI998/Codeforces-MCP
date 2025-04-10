from config import CF_API_BASE
from cf_request import make_cf_request

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