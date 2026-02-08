from pyrogram import Client
from AbhiCalls import VoiceEngine

# CONFIG
API_ID = 35362137
API_HASH = "API_HASH"
BOT_TOKEN = "BOT_TOKEN"
SESSION_STRING = "SESSION"

# Clients
bot = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user = Client(
    "music_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Voice Engine
engine = VoiceEngine(user)

# Assistant info
ASSISTANT_ID = None
ASSISTANT_USERNAME = None

