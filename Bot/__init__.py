from pyrogram import Client
from AbhiCalls import VoiceEngine

API_ID = 35362137
API_HASH = "c3c3e167ea09bc85369ca2fa3c1be790"
BOT_TOKEN = "8490783791:AAFT8DygQAO5cC-Bg6yi_D-0c7wOlIKDFdA"
SESSION_STRING = "BQBclYcAZZe_0_YNC3mOH2z2HnljeghVhYJtdRbsF7MgU7gBoqbKX0_W5HJdj4ba_gvGyEwKrkegiU6hJ38XjoIaIA69urDjjYZkWnzYtWdUcgeQkM0eKmCKanPdhz6Eqkg0D8s1kznoIFhW4T5N6yQ6DcXW7Q04GFEJRsNMSmPtNMdWWP_LXrb-WcpY4dvCkamUOw7ICqw4DPWXjtGdc36UHeClVy-DYmdVZfgipCZ50f7MirGXfb9Fx6mFqsuOYISEAx967XAZP2KRFUHV3bYHKzJDeDxB-6KQHRRazfpQGbf5WqxNbcdTTYHj2FM1GDue_75QJF05ueRQRoQh0OhRej6ghgAAAAHKUdR6AA"

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
