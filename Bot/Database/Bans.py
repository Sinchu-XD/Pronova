from pymongo.errors import DuplicateKeyError
from .Core import db
from .Stats import inc_lifetime


# ================= BAN (PER CHAT) =================
async def ban_user(chat_id, user_id):
    try:
        await db.banned.insert_one({
            "chat_id": chat_id,
            "user_id": user_id
        })
        await inc_lifetime("banned")
    except DuplicateKeyError:
        pass


async def unban_user(chat_id, user_id):
    await db.banned.delete_one({
        "chat_id": chat_id,
        "user_id": user_id
    })


async def is_banned(chat_id, user_id):
    return await db.banned.find_one({
        "chat_id": chat_id,
        "user_id": user_id
    })


async def total_banned():
    return await db.banned.count_documents({})


# ================= GBAN (GLOBAL) =================
async def gban_user(user_id):
    try:
        await db.gbanned.insert_one({"user_id": user_id})
        await inc_lifetime("gbanned")
    except DuplicateKeyError:
        pass


async def ungban_user(user_id):
    await db.gbanned.delete_one({"user_id": user_id})


async def is_gbanned(user_id):
    return await db.gbanned.find_one({"user_id": user_id})
