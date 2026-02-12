from collections import Counter
from .Core import db


# ================= TOP GROUPS =================
async def top_groups(limit: int = 10):
    res = []

    async for g in db.group_stats.find(
        {},
        {"chat_id": 1, "songs": 1}
    ).sort("songs", -1).limit(limit):

        cid = g.get("chat_id")
        songs = int(g.get("songs", 0))

        if cid and songs > 0:
            res.append((int(cid), songs))

    return res


# ================= TOP USERS =================
async def top_users(limit: int = 10):
    counter = Counter()

    async for g in db.group_stats.find(
        {},
        {"users": 1}
    ):
        users = g.get("users", {})

        if not isinstance(users, dict):
            continue

        for uid, count in users.items():
            try:
                counter[int(uid)] += int(count)
            except:
                continue

    return counter.most_common(limit)
