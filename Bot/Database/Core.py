import os
from motor.motor_asyncio import AsyncIOMotorClient


# ================= CONFIG =================
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Vexera:Vexera@vexera.wtrsmyc.mongodb.net/?appName=Vexera")
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
    await db.users.create_index("user_id", unique=True)
    await db.chats.create_index("chat_id", unique=True)
    await db.group_stats.create_index("chat_id", unique=True)
    await db.songs_stats.create_index("title", unique=True)

    await db.banned.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )

    await db.gbanned.create_index("user_id", unique=True)
    await db.daily.create_index("date", unique=True)
    await db.gc_activity.create_index("chat_id", unique=True)
    await db.afk.create_index("user_id", unique=True)
