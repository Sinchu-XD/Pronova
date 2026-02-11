from collections import Counter
from .Core import db


async def top_groups(limit=10):
    res = []
    async for g in db.group_stats.find().sort("songs", -1).limit(limit):
        res.append((g["chat_id"], g.get("songs", 0)))
    return res


async def top_users(limit=10):
    counter = Counter()
    async for g in db.group_stats.find():
        for u in g.get("users", []):
            counter[u] += 1
    return counter.most_common(limit)
  
