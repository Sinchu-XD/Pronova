import asyncio
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from Bot import bot
from Bot.Database.Users import add_user
from Bot.Helper.Font import sc


BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"

RUNNING = set()


# ===== SAFE EDIT (NO ENTITIES) =====
async def safe_edit(msg: Message, text: str, **kwargs):
    try:
        await msg.edit_text(text, **kwargs)
    except:
        pass


# ===== ANIMATION =====
async def pronova_ultimate_animation(message: Message, user_name: str):

    key = (message.chat.id, message.id)
    if key in RUNNING:
        return

    RUNNING.add(key)

    try:
        boot = [
            sc("connecting to pronova network..."),
            sc("loading audio drivers..."),
            sc("securing session..."),
            sc("system ready.")
        ]

        for phase in boot:
            await safe_edit(message, phase)
            await asyncio.sleep(0.5)

        header = sc(BOT_NAME)
        line = "⎯" * 30

        welcome = sc(f"hello {user_name}, welcome to the next era of music.")
        words = welcome.split()

        current = ""
        for w in words:
            current += w + " "
            frame = f"{header}\n{line}\n{current}▎\n{line}"
            await safe_edit(message, frame)
            await asyncio.sleep(0.12)

        dashboard = (
            f"{header}\n"
            f"{line}\n"
            f"{sc('user : premium')}\n"
            f"{sc('quality : 24-bit')}\n"
            f"{sc('latency : ultra low')}\n"
            f"{line}\n"
            f"{sc('tap below to start')}"
        )

        # 🔥 Use sc premium mode only here
        text, ent = sc("dashboard ready", premium=True)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Pronova Music To Group", url="https://t.me/ProNovaMusicBot?startgroup=true")],
            [InlineKeyboardButton("Join VIP Channel", url="https://t.me/Her4Eva")],
            [InlineKeyboardButton("Bot Owner", url="https://t.me/WtfShia")]
        ])

        await message.edit_text(dashboard, reply_markup=buttons)

    finally:
        RUNNING.discard(key)


# ===== START =====
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(_, message: Message):

    user = message.from_user
    if not user or user.is_bot:
        return

    try:
        await add_user(user)
    except:
        pass

    try:
        await message.reply_sticker(MUSIC_STICKER)
    except:
        pass

    await message.reply(sc("initializing pronova core..."))

    status = await message.reply(sc("loading system..."))

    await pronova_ultimate_animation(status, user.mention)
    
