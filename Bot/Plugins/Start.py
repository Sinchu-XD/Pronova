import asyncio
import random
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot import bot


BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕"
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
        return "Good Morning"
    if hour < 18:
        return "Good Afternoon"
    return "Good Evening"


def get_theme_line():
    themes = ["🟣", "🔵", "🟢", "🔴"]
    return random.choice(themes) * 30


def get_badge(user_id: int):
    if user_id in [123456789]:  # change owner id
        return "👑 Owner"
    return "✨ Premium"


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
⚡ **Pronova Hyper System Boot**
{line}

`Loading Modules`
[{filled}{empty}] {i}%

🧠 AI Engine : Online
💽 Memory    : Stable
📡 Network   : Connected
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
🧠 **Hardware Scan**
{line}

🎮 GPU Usage : {gpu}%
💾 RAM Usage : {ram}%
📶 Ping      : 0.0001 ms

✅ Optimized
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
🎚 **Audio Spectrum Initializing**
{line}

`{frame}`

🎧 Calibrating sound waves...
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

⏵ Status : `Ready`
🧠 AI     : `Adaptive`
🔊 Mode   : `24-Bit Ultra`
📡 Speed  : `Realtime`

{line}
✨ Tap below to continue
{line}

⚙️ Dev : {DEV_NAME}
"""

    # ✅ ONLY TWO BUTTONS
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

    status = await message.reply_text("⚡ Booting Pronova...", quote=True)
    await pronova_god_animation(status, message.from_user)
    
