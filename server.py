from typing import Any
from mcp.server.fastmcp import FastMCP
from config import CF_API_BASE
from cf_request import make_cf_request

mcp = FastMCP("codeforces-MCP")

# user    
@mcp.tool()
async def get_user_rating(handle : str) -> str :
    """
    输入Codeforces用户名, 返回该用户的rating信息
    """
    url = f"{CF_API_BASE}user.rating?handle={handle}"
    data = await make_cf_request(url)
    if type(data) == str :
        return data # 返回错误信息
    if "result" in data:
        ratings = [f"rating : {rating['newRating']}" for rating in data['result']]
        return "\n---\n".join(ratings)
    else :
        return "rusult不在data中"
    
@mcp.tool()
async def get_user_info(handle : str) -> str :
    """
    输入Codeforces用户名, 返回该用户的基本信息
    """
    url = f"{CF_API_BASE}user.info?handles={handle}"
    data = await make_cf_request(url)
    if type(data) == str :
        return data # 返回错误信息
    if "result" in data:
        user = data['result'][0]  # 获取第一个用户的信息
        info = [
            # get(查询信息， 默认值)
            f"Handle: {user['handle']}",
            f"姓名: {user.get('firstName', '')} {user.get('lastName', '')}",
            f"当前Rating: {user.get('rating', 'N/A')}",
            f"最高Rating: {user.get('maxRating', 'N/A')}",
            f"当前段位: {user.get('rank', 'N/A')}",
            f"最高段位: {user.get('maxRank', 'N/A')}",
            f"组织: {user.get('organization', '无')}",
            f"贡献度: {user.get('contribution', 0)}"
        ]
        return "\n---\n".join(info)
    else :
        return "rusult不在data中"
    
# blog 待更新

# contest 开发中
@mcp.tool() # 问题：请求超时(已解决)
async def get_contest_list(maxn : int = 50, contest_type : str = "None") -> str :
    """
    获取Codeforces可用竞赛的信息
    最近 maxn 场比赛
    contest_type : "gym" or "contest" or "None"
    """
    maxn = min(maxn, 50)  # 限制最大值为50
    
    # url 分类
    url = f"{CF_API_BASE}contest.list"
    if "gym" in contest_type.lower() :
        url += "?gym=true"
    elif "contest" in contest_type.lower() :
        url += "?contest=true"
    
    data = await make_cf_request(url)
    if type(data) == str :
        return data # 返回错误信息
    else :
        contests = []
        # 只获取后 maxn 场比赛
        for contest in data["result"][-maxn:] :
            contest_info = [
                f"比赛ID: {contest['id']}",
                f"比赛名称: {contest['name']}",
                f"比赛类型: {contest['type']}",
                f"比赛阶段: {contest['phase']}",
                f"持续时间: {contest['durationSeconds'] // 3600}小时",
                f"举办方: {contest.get('preparedBy', '未知')}",
                f"比赛性质: {contest.get('kind', '未知')}",
                f"举办国家: {contest.get('country', '未知')}",
                f"举办城市: {contest.get('city', '未知')}",
                f"赛季: {contest.get('season', '未知')}"
            ]
            contests.append("\n".join(contest_info))
        return "\n\n---\n\n".join(contests)

# prolemsets 开发中

if __name__ == "__main__" :
    mcp.run(transport='stdio')