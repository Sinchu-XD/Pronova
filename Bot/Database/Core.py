from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://Sinchu:Sinchu@sinchu.qwijj.mongodb.net/?appName=Sinchu"
DB_NAME = "Pronova"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


async def setup_database():
    await db.users.create_index("user_id", unique=True)
    await db.chats.create_index("chat_id", unique=True)
    await db.group_stats.create_index("chat_id", unique=True)
    await db.songs_stats.create_index("title", unique=True)

    # ===== FIXED BAN INDEX =====
    await db.banned.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )

    # global ban correct
    await db.gbanned.create_index("user_id", unique=True)

    await db.daily.create_index("date", unique=True)
    await db.gc_activity.create_index("chat_id", unique=True)
    await db.afk.create_index("user_id", unique=True)
