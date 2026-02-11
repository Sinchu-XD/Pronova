from .Core import db
from .Stats import inc_lifetime, inc_daily


async def inc_song_play(chat_id=None, title=None):
    await inc_lifetime("songs")
    await inc_daily("songs")

    if chat_id:
        await db.group_stats.update_one(
            {"chat_id": chat_id},
            {"$inc": {"songs": 1}},
            upsert=True,
        )

    if title:
        await db.songs_stats.update_one(
            {"title": title},
            {"$inc": {"played": 1}},
            upsert=True,
        )


async def most_played(limit=10):
    res = []
    async for s in db.songs_stats.find().sort("played", -1).limit(limit):
        res.append((s["title"], s.get("played", 0)))
    return res
  
