from .Core import db
from .Stats import inc_lifetime, inc_daily


# ================= NORMALIZE =================
def normalize_title(title: str) -> str:
    return title.lower().strip()


# ================= INC PLAY =================
async def inc_song_play(chat_id=None, title=None):
    await inc_lifetime("songs")
    await inc_daily("songs")

    # group counter
    if chat_id:
        await db.group_stats.update_one(
            {"chat_id": chat_id},
            {"$inc": {"songs": 1}},
            upsert=True,
        )

    # song counter
    if title:
        title = normalize_title(title)

        if not title:
            return

        await db.songs_stats.update_one(
            {"title": title},
            {"$inc": {"played": 1}},
            upsert=True,
        )


# ================= MOST PLAYED =================
async def most_played(limit: int = 10):
    res = []

    async for s in db.songs_stats.find(
        {},
        {"title": 1, "played": 1}
    ).sort("played", -1).limit(limit):

        res.append((
            s.get("title", "unknown"),
            int(s.get("played", 0))
        ))

    return res
