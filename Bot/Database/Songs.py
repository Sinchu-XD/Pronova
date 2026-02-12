from .Core import db
from .Stats import inc_lifetime, inc_daily


# ================= NORMALIZE =================
def normalize_title(title: str) -> str:
    if not title:
        return ""
    return str(title).lower().strip()


# ================= UTILS =================
def _to_int(x):
    try:
        return int(x.id) if not isinstance(x, int) else int(x)
    except:
        return None


# ================= INC PLAY =================
async def inc_song_play(chat=None, title=None):
    # ===== global counters =====
    await inc_lifetime("songs")
    await inc_daily("songs")

    # ===== group counter =====
    cid = _to_int(chat)
    if cid:
        await db.group_stats.update_one(
            {"chat_id": cid},
            {"$inc": {"songs": 1}},
            upsert=True,
        )

    # ===== song counter =====
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

        try:
            title = s.get("title", "unknown")
            played = int(s.get("played", 0))
        except:
            continue

        if played > 0:
            res.append((title, played))

    return res
    
