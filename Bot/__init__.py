import os
from pyrogram import Client
from AbhiCalls import VoiceEngine


# ================= CONFIG =================
API_ID = 35362137
API_HASH = "c3c3e167ea09bc85369ca2fa3c1be790"
BOT_TOKEN = "8490783791:AAFT8DygQAO5cC-Bg6yi_D-0c7wOlIKDFdA"
SESSION_STRING = "BQG9G9UArCL3soXNEboELJrQCJsNl4ivCTeB3uh81u0fPGg7v_po-FCjDaqSATbBLu3FfuCUcPvqIQGmhH7wbfLS3TpGXvW-OAo-uZR6vJIQPfXQjd6dmOceor8eQshk5-3MsKKEI8HOnmFoAV-9bK-yweT_VY0nOCzJ_iJqkmlqgEYOMfnhDCSDDvHaVO2rd8V8qVp1wW0RUKEEQ267rkPEKhXHvCBTgRp29CJJA1tyqQvreDep7sw60XCYFHYsm1xK1tqKiGNaeGMtmQRegzmTEZuwOgVqwFiu4jnqXwJ-UCa0a4pLcLXdzva0ZzJECL0nwYgTFgFJ5gWqaLL1yKJSBa1ElAAAAAHKUdR6AA"
COOKIES = "cookies.txt"


# ================= VALIDATION =================
if not API_ID or not API_HASH or not BOT_TOKEN or not SESSION_STRING:
    raise RuntimeError("Missing required environment variables")

# ================= CUSTOM EMOJI IDS =================
CUSTOM_EMOJI_IDS = [
    6089195853908548095,
    6334453153823459140,
    6334525760245597578,
    6334832949191509666,
    6334540251465254516,
    6334555537253860831,
    6332440708242212451,
    6097980951814475221,
    6334719188392740438,
    6269122341859495184,
    6271346172846149465,
    6271719066201755333,
    6217467341421154237,
    6237977283433338540,
    6235677650568878393,
    6113826782681502268,
    6116320024081731477
]

# ================= CLIENTS =================
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


# ================= ENGINE =================
engine = VoiceEngine(user, cookies=COOKIES)
