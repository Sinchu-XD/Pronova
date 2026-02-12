from .Core import db
from .Stats import inc_lifetime


# ================= UTILS =================
def _to_int(x):
    try:
        return int(x.id) if not isinstance(x, int) else int(x)
    except:
        return None


# ================= BAN (PER CHAT) =================
async def ban_user(chat, user):
    cid = _to_int(chat)
    uid = _to_int(user)

    if not cid or not uid:
        return

    result = await db.banned.update_one(
        {"chat_id": cid, "user_id": uid},
        {"$setOnInsert": {"chat_id": cid, "user_id": uid}},
        upsert=True,
    )

    if result.upserted_id:
        await inc_lifetime("banned")


async def unban_user(chat, user):
    cid = _to_int(chat)
    uid = _to_int(user)

    if not cid or not uid:
        return

    await db.banned.delete_one({"chat_id": cid, "user_id": uid})


async def is_banned(chat, user):
    cid = _to_int(chat)
    uid = _to_int(user)

    if not cid or not uid:
        return False

    data = await db.banned.find_one(
        {"chat_id": cid, "user_id": uid},
        {"_id": 1}
    )
    return bool(data)


async def get_banned(chat):
    cid = _to_int(chat)

    if not cid:
        return []

    users = []

    async for x in db.banned.find(
        {"chat_id": cid},
        {"user_id": 1}
    ):
        try:
            users.append(int(x.get("user_id")))
        except:
            continue

    return users


async def total_banned():
    return await db.banned.count_documents({})


# ================= GBAN (GLOBAL) =================
async def gban_user(user):
    uid = _to_int(user)

    if not uid:
        return

    result = await db.gbanned.update_one(
        {"user_id": uid},
        {"$setOnInsert": {"user_id": uid}},
        upsert=True,
    )

    if result.upserted_id:
        await inc_lifetime("gbanned")


async def ungban_user(user):
    uid = _to_int(user)

    if not uid:
        return

    await db.gbanned.delete_one({"user_id": uid})


async def is_gbanned(user):
    uid = _to_int(user)

    if not uid:
        return False

    data = await db.gbanned.find_one(
        {"user_id": uid},
        {"_id": 1}
    )
    return bool(data)


async def get_gbanned():
    users = []

    async for x in db.gbanned.find({}, {"user_id": 1}):
        try:
            users.append(int(x.get("user_id")))
        except:
            continue

    return users
    
