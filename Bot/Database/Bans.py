from .Core import db
from .Stats import inc_lifetime


# ================= BAN (PER CHAT) =================
async def ban_user(chat_id, user_id):
    if not chat_id or not user_id:
        return

    cid = int(chat_id)
    uid = int(user_id)

    result = await db.banned.update_one(
        {"chat_id": cid, "user_id": uid},
        {"$setOnInsert": {"chat_id": cid, "user_id": uid}},
        upsert=True,
    )

    # count only if new ban
    if result.upserted_id:
        await inc_lifetime("banned")


async def unban_user(chat_id, user_id):
    if not chat_id or not user_id:
        return

    await db.banned.delete_one({
        "chat_id": int(chat_id),
        "user_id": int(user_id)
    })


async def is_banned(chat_id, user_id):
    if not chat_id or not user_id:
        return False

    data = await db.banned.find_one(
        {"chat_id": int(chat_id), "user_id": int(user_id)},
        {"_id": 1}
    )
    return bool(data)


async def get_banned(chat_id):
    if not chat_id:
        return []

    users = []

    async for x in db.banned.find(
        {"chat_id": int(chat_id)},
        {"user_id": 1}
    ):
        users.append(int(x.get("user_id")))

    return users


async def total_banned():
    return await db.banned.count_documents({})


# ================= GBAN (GLOBAL) =================
async def gban_user(user_id):
    if not user_id:
        return

    uid = int(user_id)

    result = await db.gbanned.update_one(
        {"user_id": uid},
        {"$setOnInsert": {"user_id": uid}},
        upsert=True,
    )

    if result.upserted_id:
        await inc_lifetime("gbanned")


async def ungban_user(user_id):
    if not user_id:
        return

    await db.gbanned.delete_one({"user_id": int(user_id)})


async def is_gbanned(user_id):
    if not user_id:
        return False

    data = await db.gbanned.find_one(
        {"user_id": int(user_id)},
        {"_id": 1}
    )
    return bool(data)


async def get_gbanned():
    users = []

    async for x in db.gbanned.find({}, {"user_id": 1}):
        users.append(int(x.get("user_id")))

    return users
    
