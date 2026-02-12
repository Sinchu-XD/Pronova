from .Core import db


# ================= UPDATE =================
async def update_gc_activity(chat, user):
    if not chat or not user:
        return

    # allow object or int
    try:
        cid = int(chat.id) if not isinstance(chat, int) else int(chat)
        uid = int(user.id) if not isinstance(user, int) else int(user)
    except:
        return

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
async def get_gc_activity(chat):
    if not chat:
        return {"users": {}, "total_messages": 0}

    try:
        cid = int(chat.id) if not isinstance(chat, int) else int(chat)
    except:
        return {"users": {}, "total_messages": 0}

    data = await db.gc_activity.find_one(
        {"chat_id": cid},
        {"users": 1, "total_messages": 1}
    )

    if not data:
        return {"users": {}, "total_messages": 0}

    users = data.get("users", {})

    if not isinstance(users, dict):
        users = {}

    try:
        total = int(data.get("total_messages", 0))
    except:
        total = 0

    return {
        "users": users,
        "total_messages": total
    }
