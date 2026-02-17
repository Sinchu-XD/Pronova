import os
from pyrogram import Client
from AbhiCalls import VoiceEngine


# ================= CONFIG =================
API_ID = 35362137
API_HASH = "c3c3e167ea09bc85369ca2fa3c1be790"
BOT_TOKEN = "8490783791:AAFT8DygQAO5cC-Bg6yi_D-0c7wOlIKDFdA"
SESSION_STRING = "BQG9G9UAmBz34sNcK6BJTtseRg_A5jAC96GBihFN655Iq8Umf1k-pI5gi4-qPEraQ3c0S5HrYadMuATWqF9em45zJyqkZoZGuSAyzZmXBedGj_eUxRkqX_LofHmAhDtQposU4X-62_xMv-5SeZuRBoTsWqs300pd9TY8i9Y9NuBHmm5ywibFc8w02NEJqgznBkJpDuuAAsp6cSFFOQRBYvUkULS4f0wofmW9uEey6JQ4vIX9g2WwsrDXwqSNWtYKK9gJyjzyspbwqQGEyLrlc6UXgO_Wtds6kS3mgOO--vIXO7Z-yYsJH9bqc5VhlHaVSc9UcaAP81zD2NIhhOG1FmY6FJ_MVwAAAAHKUdR6AA"
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
