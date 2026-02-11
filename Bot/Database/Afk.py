from datetime import datetime
from .Core import db


# ================= SET =================
async def set_afk_db(user_id, reason):
    if not user_id:
        return

    uid = int(user_id)

    await db.afk.update_one(
        {"user_id": uid},
        {
            "$set": {
                "reason": reason,
                "since": datetime.utcnow()
            }
        },
        upsert=True,
    )


# ================= REMOVE =================
async def remove_afk_db(user_id):
    if not user_id:
        return

    await db.afk.delete_one({"user_id": int(user_id)})


# ================= GET =================
async def get_afk(user_id):
    if not user_id:
        return None

    return await db.afk.find_one(
        {"user_id": int(user_id)},
        {"reason": 1, "since": 1}
    )
