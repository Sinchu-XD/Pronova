from pyrogram import Client
from AbhiCalls import VoiceEngine

API_ID = 35362137
API_HASH = "API_HASH"
BOT_TOKEN = "BOT_TOKEN"
SESSION_STRING = "SESSION"

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

engine = VoiceEngine(user)
