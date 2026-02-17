import os
from pyrogram import Client
from AbhiCalls import VoiceEngine


# ================= CONFIG =================
API_ID = 35362137
API_HASH = "c3c3e167ea09bc85369ca2fa3c1be790"
BOT_TOKEN = "8490783791:AAFT8DygQAO5cC-Bg6yi_D-0c7wOlIKDFdA"
SESSION_STRING = "BQG9G9UAnrN02DVHcJeoV34xCrIDd-wcM_t9EO0x31O-hZPG7VOr4_mrlX3Hnx3XcImbhUfURkMRfOSDKJvqNaLrr3o5NsozGm67DLMG7W6ikkCD8PQYcurTWsD1qutO8t0d83m9L3ItEq4NppYQ9wspZxMBanlcQEgf3t1YyyULLQK0-CSK-s7Belv7oqXjb-4aBC9eWnseGjY7gz11g9zbMBxeT2rDNyhggorlLpdPARY03R6ucN2fOnJCOdtbKKKr-4ptBkhhHXmUsILekVMrhNxJCCTkOolPautyOn7sZ8vEyy0sCPWwnMnmZ-KxSkzVS6s1dILaFc8TYmcu_a2uZ8wg-QAAAAHKUdR6AA"
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
