from collections import Counter
from .Core import db


# ================= TOP GROUPS =================
async def top_groups(limit: int = 10):
    res = []

    async for g in db.group_stats.find(
        {},
        {"chat_id": 1, "songs": 1}
    ).sort("songs", -1).limit(limit):

        res.append((
            g.get("chat_id"),
            int(g.get("songs", 0))
        ))

    return res


# ================= TOP USERS =================
async def top_users(limit: int = 10):
    counter = Counter()

    async for g in db.group_stats.find(
        {},
        {"users": 1}
    ):
        users = g.get("users", {})

        # ensure dictionary
        if isinstance(users, dict):
            for uid in users.keys():
                counter[int(uid)] += 1

    return counter.most_common(limit)
