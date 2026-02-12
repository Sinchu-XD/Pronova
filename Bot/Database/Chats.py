from datetime import datetime
from .Core import db
from .Stats import inc_lifetime, inc_daily


# ================= ADD CHAT =================
async def add_chat(chat):
    if not chat:
        return

    # ===== accept both id and object =====
    if isinstance(chat, int):
        cid = int(chat)
    else:
        cid = int(chat.id)

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

    # ===== count only if new =====
    if result.upserted_id:
        await inc_lifetime("chats")
        await inc_daily("chats")


# ================= TOTAL =================
async def total_chats():
    return await db.chats.count_documents({})


# ================= GET ALL =================
async def get_all_chats():
    async for c in db.chats.find({}, {"chat_id": 1}):
        yield int(c.get("chat_id"))
