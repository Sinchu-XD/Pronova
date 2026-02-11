from datetime import datetime
from .Core import db
from .Stats import inc_lifetime


# ================= ADD CHAT =================
async def add_chat(chat_id):
    if not chat_id:
        return

    cid = int(chat_id)

    result = await db.chats.update_one(
        {"chat_id": cid},
        {
            "$setOnInsert": {
                "chat_id": cid,
                "join_date": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    # only if new
    if result.upserted_id:
        await inc_lifetime("chats")


# ================= TOTAL =================
async def total_chats():
    return await db.chats.count_documents({})


# ================= GET ALL =================
async def get_all_chats():
    async for c in db.chats.find({}, {"chat_id": 1}):
        yield int(c.get("chat_id"))
