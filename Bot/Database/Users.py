from datetime import datetime
from pymongo.errors import DuplicateKeyError
from .Core import db
from .Stats import inc_lifetime, inc_daily


async def add_user(user):
    if not user or user.is_bot:
        return

    try:
        await db.users.insert_one({
            "user_id": user.id,
            "join_date": datetime.utcnow(),
        })
        await inc_lifetime("users")
        await inc_daily("users")
    except DuplicateKeyError:
        pass


async def total_users():
    return await db.users.count_documents({})


async def get_users():
    async for u in db.users.find({}):
        yield u["user_id"]
      
