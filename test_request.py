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

async def get_user_performance_in_contest(handle : str, contest_id : int) -> str :
    """
    获取用户在某场比赛中的表现
    handle : 用户名
    contest_id : 比赛ID
    """
    url = f"{CF_API_BASE}contest.ratingChanges?contestId={contest_id}"
    data = await make_cf_request(url)
    
    if type(data) == str:
        return data  # 返回错误信息
    
    for performance in data["result"]:
        if performance["handle"].lower() == handle.lower():
            performance_info = [
                f"比赛ID: {performance['contestId']}",
                f"比赛名称: {performance['contestName']}",
                f"用户名: {performance['handle']}",
                f"排名: {performance['rank']}",
                # f"比赛时间: {performance['ratingUpdateTimeSeconds'] }",
                f"旧Rating: {performance['oldRating']}",
                f"新Rating: {performance['newRating']}"
            ]
            return "\n".join(performance_info)
    
    return f"未找到用户 {handle} 在比赛 {contest_id} 中的表现信息。"

async def get_problems_in_tag(tag : str) -> str : # 开发中，暂未测试
    """
    获取某个标签下的题目
    tag : 标签名
    """
    url = f"{CF_API_BASE}problemset.problems?tags={tag}"

    if "implementation" in tag.lower() :
        url += "&tags=implementation"

    data = await make_cf_request(url)
    
    if type(data) == str:
        return data  # 返回错误信息
    
    problems = []
    for problem in data["result"]["problems"]:
        # 检查题目是否包含指定标签
        if tag in problem["tags"]:
            problem_info = [
                f"题目ID: {problem['contestId']}{problem['index']}",
                f"题目名称: {problem['name']}",
                f"题目类型: {problem['type']}",
                f"题目标签: {', '.join(problem['tags'])}",
                f"题目难度: {problem.get('rating', '未知')}",
                f"分数: {problem.get('points', '未知')}"
            ]
            problems.append("\n".join(problem_info))
    
    if not problems:
        return f"未找到包含标签 '{tag}' 的题目。"
    
    return "\n\n---\n\n".join(problems)

async def main() :
    print("hello!")
    result = await get_user_performance_in_contest("Octagons", 2093)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())