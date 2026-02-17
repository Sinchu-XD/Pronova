import asyncio
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from Bot import bot
from Bot.Helper.Font import sc
from Bot.Helper.Emoji import add_premium
from Bot.Database.Users import add_user


BOT_NAME = "Pronova Music Bot"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"

RUNNING = set()


# ================= SAFE EDIT =================
async def safe_edit(msg: Message, text: str):
    try:
        await msg.edit_text(text)
    except:
        pass


# ================= ANIMATION =================
async def pronova_ultimate_animation(message: Message, user):

    key = (message.chat.id, message.id)
    if key in RUNNING:
        return

    RUNNING.add(key)

    try:
        boot = [
            sc("connecting to pronova network"),
            sc("loading audio drivers"),
            sc("securing session"),
            sc("system ready")
        ]

        for phase in boot:
            await safe_edit(message, phase)
            await asyncio.sleep(0.5)

        header = sc(BOT_NAME)
        line = "⎯" * 30

        welcome_line = sc(f"hello {user.first_name}, welcome to the next era of music")
        frame = f"{header}\n{line}\n{welcome_line}\n{line}"

        await safe_edit(message, frame)
        await asyncio.sleep(1)

        dashboard = (
            f"{header}\n"
            f"{line}\n"
            f"{sc('user')} : Premium\n"
            f"{sc('quality')} : 24-bit\n"
            f"{sc('latency')} : Ultra Low\n"
            f"{line}\n"
            f"{sc('tap below to start')}"
        )

        dashboard, ent = add_premium(dashboard)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Pronova Music To Group", url="https://t.me/ProNovaMusicBot?startgroup=true")],
            [InlineKeyboardButton("Join VIP Channel", url="https://t.me/Her4Eva")],
            [InlineKeyboardButton("Bot Owner", url="https://t.me/WtfShia")]
        ])

        await message.edit_text(
            dashboard,
            entities=ent,
            reply_markup=buttons
        )

    finally:
        RUNNING.discard(key)

    
# ================= START COMMAND =================
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

    await message.reply(sc("initializing pronova core"))

    status = await message.reply(sc("loading system"))

    await pronova_ultimate_animation(status, user)
    
