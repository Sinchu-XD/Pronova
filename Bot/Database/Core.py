import os
from motor.motor_asyncio import AsyncIOMotorClient


# ================= CONFIG =================
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Sinchu:Sinchu@sinchu.qwijj.mongodb.net/?appName=Sinchu")
DB_NAME = os.getenv("DB_NAME", "Pronova")


# ================= CLIENT =================
client = AsyncIOMotorClient(
    MONGO_URL,
    maxPoolSize=100,
    minPoolSize=10,
    serverSelectionTimeoutMS=5000,
)

db = client[DB_NAME]


# ================= SETUP =================
async def setup_database():
    # users / chats
    await db.users.create_index("user_id", unique=True, name="user_id_unique")
    await db.chats.create_index("chat_id", unique=True, name="chat_id_unique")

    # stats
    await db.group_stats.create_index("chat_id", unique=True, name="group_unique")
    await db.songs_stats.create_index("title", unique=True, name="song_unique")

    # bans
    await db.banned.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True,
        name="chat_user_ban_unique"
    )
    await db.gbanned.create_index("user_id", unique=True, name="gban_unique")

    # analytics
    await db.daily.create_index("date", unique=True, name="daily_unique")
    await db.gc_activity.create_index("chat_id", unique=True, name="gc_unique")

    # afk
    await db.afk.create_index("user_id", unique=True, name="afk_unique")
