from datetime import datetime
from .Core import db
from .Stats import inc_lifetime, inc_daily


# ================= ADD USER =================
async def add_user(user):
    if not user:
        return

    # ===== accept both int and user object =====
    if isinstance(user, int):
        uid = int(user)
    else:
        # ignore bots
        if getattr(user, "is_bot", False):
            return
        uid = int(user.id)

    result = await db.users.update_one(
        {"user_id": uid},
        {
            "$setOnInsert": {
                "user_id": uid,
                "join_date": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    # ===== increase counters only if new =====
    if result.upserted_id:
        await inc_lifetime("users")
        await inc_daily("users")


# ================= TOTAL =================
async def total_users():
    return await db.users.count_documents({})


# ================= GET USERS =================
async def get_users():
    async for u in db.users.find({}, {"user_id": 1}):
        yield int(u.get("user_id"))


# ================= REMOVE USER =================
async def remove_user(user_id):
    if not user_id:
        return

    await db.users.delete_one({"user_id": int(user_id)})
    
