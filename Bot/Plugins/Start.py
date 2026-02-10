import asyncio
import random
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot import bot


# Mixed Font Brand
BOT_NAME = "𝗣𝗿𝗼𝗻𝗼𝘃𝗮 𝑴𝒖𝒔𝗶𝗰 𝗕𝗼𝘁"
DEV_NAME = "Abhi"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"

_last_text_cache = {}


# ==========================
# SAFE EDIT
# ==========================
async def safe_edit(msg: Message, text: str, **kwargs):
    key = (msg.chat.id, msg.id)

    if _last_text_cache.get(key) == text:
        return

    try:
        await msg.edit_text(text, **kwargs)
        _last_text_cache[key] = text
    except Exception:
        pass


# ==========================
# HELPERS
# ==========================
def get_greeting():
    hour = datetime.utcnow().hour
    if hour < 12:
        return "𝗚𝗼𝗼𝗱 𝗠𝗼𝗿𝗻𝗶𝗻𝗴"
    if hour < 18:
        return "𝗚𝗼𝗼𝗱 𝗔𝗳𝘁𝗲𝗿𝗻𝗼𝗼𝗻"
    return "𝗚𝗼𝗼𝗱 𝗘𝘃𝗲𝗻𝗶𝗻𝗴"


def get_theme_line():
    themes = ["🟣", "🔵", "🟢", "🔴"]
    return random.choice(themes) * 30


def get_badge(user_id: int):
    if user_id in [6444277321]:
        return "👑 𝗢𝘄𝗻𝗲𝗿"
    return "✨ 𝗣𝗿𝗲𝗺𝗶𝘂𝗺"


# ==========================
# GOD LEVEL ANIMATION
# ==========================
async def pronova_god_animation(message: Message, user):
    print("[StartUI] GOD animation start")

    greeting = get_greeting()
    badge = get_badge(user.id)
    line = get_theme_line()

    # ================= Loader =================
    for i in range(0, 101, 10):
        filled = "█" * (i // 10)
        empty = "░" * (10 - i // 10)

        await safe_edit(
            message,
            f"""
{line}
⚡ **𝗣𝗿𝗼𝗻𝗼𝘃𝗮 𝗛𝘆𝗽𝗲𝗿 𝗦𝘆𝘀𝘁𝗲𝗺 𝗕𝗼𝗼𝘁**
{line}

`𝗟𝗼𝗮𝗱𝗶𝗻𝗴 𝗠𝗼𝗱𝘂𝗹𝗲𝘀`
[{filled}{empty}] {i}%

🧠 𝗔𝗜 𝗘𝗻𝗴𝗶𝗻𝗲 : `Online`
💽 𝗠𝗲𝗺𝗼𝗿𝘆    : `Stable`
📡 𝗡𝗲𝘁𝘄𝗼𝗿𝗸   : `Connected`
""",
        )
        await asyncio.sleep(0.25)

    # ================= Hardware =================
    gpu = random.randint(40, 90)
    ram = random.randint(30, 80)

    await safe_edit(
        message,
        f"""
{line}
🧠 **𝗛𝗮𝗿𝗱𝘄𝗮𝗿𝗲 𝗦𝗰𝗮𝗻**
{line}

🎮 𝗚𝗣𝗨 : `{gpu}%`
💾 𝗥𝗔𝗠 : `{ram}%`
📶 𝗣𝗶𝗻𝗴: `0.0001 ms`

✅ 𝗢𝗽𝘁𝗶𝗺𝗶𝘇𝗲𝗱
""",
    )
    await asyncio.sleep(1)

    # ================= Equalizer =================
    eq_frames = [
        "▁ ▂ ▃ ▄ ▅ ▆ ▇",
        "▇ ▆ ▅ ▄ ▃ ▂ ▁",
        "▂ ▄ ▆ ▇ ▆ ▄ ▂",
        "▃ ▅ ▇ ▅ ▃ ▂ ▁",
    ]

    for _ in range(2):
        for frame in eq_frames:
            await safe_edit(
                message,
                f"""
{line}
🎚 **𝗔𝘂𝗱𝗶𝗼 𝗦𝗽𝗲𝗰𝘁𝗿𝘂𝗺 𝗜𝗻𝗶𝘁𝗶𝗮𝗹𝗶𝘇𝗶𝗻𝗴**
{line}

`{frame}`

🎧 𝗖𝗮𝗹𝗶𝗯𝗿𝗮𝘁𝗶𝗻𝗴...
""",
            )
            await asyncio.sleep(0.25)

    # ================= FINAL DASHBOARD =================
    dashboard = f"""
{line}
👋 **{greeting}, {user.mention}**
{line}

🎧 **{BOT_NAME}**
{badge}

⏵ 𝗦𝘁𝗮𝘁𝘂𝘀 : `Ready`
🧠 𝗔𝗜     : `Adaptive`
🔊 𝗠𝗼𝗱𝗲   : `24-Bit Ultra`
📡 𝗦𝗽𝗲𝗲𝗱  : `Realtime`

{line}
✨ 𝗧𝗮𝗽 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲
{line}

⚙️ 𝗗𝗲𝘃 : {DEV_NAME}
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add To Group",
                url="https://t.me/ProNovaMusicBot?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 VIP Channel",
                url="https://t.me/Her4Eva"
            )
        ]
    ])

    await safe_edit(message, dashboard, reply_markup=buttons)

    print("[StartUI] GOD animation end")


# ==========================
# START
# ==========================
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    print("[StartUI] /start")

    try:
        await message.reply_sticker(MUSIC_STICKER)
    except Exception:
        pass

    status = await message.reply_text("⚡ 𝗕𝗼𝗼𝘁𝗶𝗻𝗴 𝗣𝗿𝗼𝗻𝗼𝘃𝗮...", quote=True)
    await pronova_god_animation(status, message.from_user)
    
