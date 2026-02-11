from datetime import datetime
from pymongo.errors import DuplicateKeyError
from .Core import db


# set afk
async def set_afk_db(user_id, reason):
    try:
        await db.afk.insert_one({
            "user_id": user_id,
            "reason": reason,
            "since": datetime.utcnow()
        })
    except DuplicateKeyError:
        await db.afk.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "reason": reason,
                    "since": datetime.utcnow()
                }
            }
        )


# remove
async def remove_afk_db(user_id):
    await db.afk.delete_one({"user_id": user_id})


# get
async def get_afk(user_id):
    return await db.afk.find_one({"user_id": user_id})
  
