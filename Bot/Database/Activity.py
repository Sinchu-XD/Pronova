from .Core import db


async def update_gc_activity(chat_id, user_id):
    await db.gc_activity.update_one(
        {"chat_id": chat_id},
        {
            "$inc": {
                f"users.{user_id}": 1,
                "total_messages": 1,
            }
        },
        upsert=True,
    )


async def get_gc_activity(chat_id):
    return await db.gc_activity.find_one({"chat_id": chat_id})
  
