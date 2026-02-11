from datetime import datetime
from pymongo.errors import DuplicateKeyError
from .Core import db
from .Stats import inc_lifetime


async def add_chat(chat_id):
    try:
        await db.chats.insert_one({
            "chat_id": chat_id,
            "join_date": datetime.utcnow(),
        })
        await inc_lifetime("chats")
    except DuplicateKeyError:
        pass


async def total_chats():
    return await db.chats.count_documents({})
  
