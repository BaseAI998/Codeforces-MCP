import httpx
from config import CF_API_BASE
from cf_request import make_cf_request
import asyncio

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

async def main() :
    print("hello!")
    maxn = int(input("please give me the maxn : "))
    contest_type = input("please give me the type : ")
    result = await get_contest_list(maxn=maxn, contest_type=contest_type)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())