from datetime import datetime
from .Core import db


# ================= SET =================
async def set_afk_db(user, reason=None):
    if not user:
        return

    # accept id or object
    try:
        uid = int(user.id) if not isinstance(user, int) else int(user)
    except:
        return

    if not reason:
        reason = "AFK"

    await db.afk.update_one(
        {"user_id": uid},
        {
            "$set": {
                "reason": str(reason),
                "since": datetime.utcnow()
            }
        },
        upsert=True,
    )


# ================= REMOVE =================
async def remove_afk_db(user):
    if not user:
        return

    try:
        uid = int(user.id) if not isinstance(user, int) else int(user)
    except:
        return

    await db.afk.delete_one({"user_id": uid})


# ================= GET =================
async def get_afk(user):
    if not user:
        return None

    try:
        uid = int(user.id) if not isinstance(user, int) else int(user)
    except:
        return None

    data = await db.afk.find_one(
        {"user_id": uid},
        {"reason": 1, "since": 1}
    )

    if not data:
        return None

    return {
        "reason": data.get("reason", "AFK"),
        "since": data.get("since")
    }
    
