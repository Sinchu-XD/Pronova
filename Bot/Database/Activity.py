from .Core import db


# ================= UPDATE =================
async def update_gc_activity(chat_id, user_id):
    if not chat_id or not user_id:
        return

    cid = int(chat_id)
    uid = int(user_id)

    await db.gc_activity.update_one(
        {"chat_id": cid},
        {
            "$inc": {
                f"users.{uid}": 1,
                "total_messages": 1,
            }
        },
        upsert=True,
    )


# ================= GET =================
async def get_gc_activity(chat_id):
    if not chat_id:
        return {"users": {}, "total_messages": 0}

    data = await db.gc_activity.find_one(
        {"chat_id": int(chat_id)},
        {"users": 1, "total_messages": 1}
    )

    if not data:
        return {"users": {}, "total_messages": 0}

    return {
        "users": data.get("users", {}),
        "total_messages": int(data.get("total_messages", 0))
    }
    
