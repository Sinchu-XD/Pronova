import asyncio
import random
from pyrogram import filters, enums
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MessageEntity
)

from Bot import bot, CUSTOM_EMOJI_IDS
from Bot.Database.Users import add_user


BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"

RUNNING = set()


# ================= PREMIUM INJECTOR =================
def inject_premium(text: str):
    lines = text.split("\n")
    final_text = ""
    entities = []
    offset = 0

    for line in lines:
        emoji_id = random.choice(CUSTOM_EMOJI_IDS)

        new_line = line + " ❤️"
        final_text += new_line + "\n"

        entities.append(
            MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset + len(new_line) - 1,
                length=1,
                custom_emoji_id=emoji_id
            )
        )

        offset += len(new_line) + 1

    final_text = final_text.rstrip("\n")
    return final_text, entities


# ================= SAFE EDIT =================
async def safe_edit(msg: Message, text: str, **kwargs):
    try:
        text, ent = inject_premium(text)
        await msg.edit_text(text, entities=ent, **kwargs)
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" in str(e):
            return
        print("[StartUI Edit]", e)


# ================= ANIMATION =================
async def pronova_ultimate_animation(message: Message, user_name: str):
    key = (message.chat.id, message.id)

    if key in RUNNING:
        return

    RUNNING.add(key)

    try:
        # ===== Boot Phases =====
        boot_phases = [
            "ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴘʀᴏɴᴏᴠᴀ ɴᴇᴛᴡᴏʀᴋ...",
            "ʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ ᴅʀɪᴠᴇʀs...",
            "sᴇᴄᴜʀɪɴɢ sᴇssɪᴏɴ...",
            "sʏsᴛᴇᴍ ʀᴇᴀᴅʏ."
        ]

        for phase in boot_phases:
            await safe_edit(message, phase)
            await asyncio.sleep(0.5)

        header = BOT_NAME
        line = "⎯" * 30

        # ===== Word Animation =====
        welcome_text = f"ʜᴇʟʟᴏ {user_name}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴇʀᴀ ᴏꜰ ᴍᴜsɪᴄ."
        words = welcome_text.split()

        current = ""
        for word in words:
            current += word + " "
            animated = (
                f"{header}\n"
                f"{line}\n"
                f"{current}▎\n"
                f"{line}"
            )
            await safe_edit(message, animated)
            await asyncio.sleep(0.12)

        # ===== Final Dashboard =====
        dashboard = (
            f"{header}\n"
            f"{line}\n"
            "●─────────── 𝟶𝟻:𝟸𝟶\n"
            "⇆   ◁   ❚❚   ▷   ↻\n"
            f"{line}\n"
            "ᴜsᴇʀ : ᴘʀᴇᴍɪᴜᴍ\n"
            "ǫᴜᴀʟɪᴛʏ : 𝟸𝟺-ʙɪᴛ\n"
            "ʟᴀᴛᴇɴᴄʏ : ᴜʟᴛʀᴀ ʟᴏᴡ\n"
            f"{line}\n"
            "ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴀᴅᴅ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 ᴛᴏ ɢʀᴏᴜᴘ", url="https://t.me/ProNovaMusicBot?startgroup=true")],
            [InlineKeyboardButton("ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Her4Eva")],
            [InlineKeyboardButton("👑 ʙᴏᴛ ᴏᴡɴᴇʀ", url="https://t.me/WtfShia")]
        ])

        await safe_edit(message, dashboard, reply_markup=buttons)

    finally:
        RUNNING.discard(key)


# ================= START =================
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(_, message: Message):
    user = message.from_user

    if not user or user.is_bot:
        return

    try:
        await add_user(user)
    except Exception as e:
        print("START STATS FAIL:", e)

    try:
        await message.reply_sticker(MUSIC_STICKER)
    except:
        pass

    init_text, ent = inject_premium("ɪɴɪᴛɪᴀʟɪᴢɪɴɢ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑪𝒐𝒓𝒆...")
    status_msg = await message.reply_text(init_text, entities=ent)

    await pronova_ultimate_animation(status_msg, user.mention)
    
