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


# ===== SAFE EDIT =====
async def safe_edit(msg: Message, text: str):
    try:
        await msg.edit_text(text)
    except:
        pass


# ===== ANIMATION =====
async def pronova_ultimate_animation(message: Message, user):

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

        # ✅ No split on mention
        welcome_line = f"{sc('hello')} {user.mention}, {sc('welcome to the next era of music.')}"
        frame = f"{header}\n{line}\n{welcome_line}\n{line}"

        await safe_edit(message, frame)
        await asyncio.sleep(1)

        dashboard_plain = (
            f"{header}\n"
            f"{line}\n"
            f"{sc('user : premium')}\n"
            f"{sc('quality : 24-bit')}\n"
            f"{sc('latency : ultra low')}\n"
            f"{line}\n"
            f"{sc('tap below to start')}"
        )

        text, ent = sc(dashboard_plain, premium=True)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Pronova Music To Group", url="https://t.me/ProNovaMusicBot?startgroup=true")],
            [InlineKeyboardButton("Join VIP Channel", url="https://t.me/Her4Eva")],
            [InlineKeyboardButton("Bot Owner", url="https://t.me/WtfShia")]
        ])

        await message.edit_text(
            text,
            entities=ent,
            reply_markup=buttons
        )

    finally:
        RUNNING.discard(key)


# ===== START COMMAND =====
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

    await pronova_ultimate_animation(status, user)
    
