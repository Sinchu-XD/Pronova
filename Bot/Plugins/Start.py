import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Bot import bot
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat


BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕🌷"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"


# prevent duplicate animations
RUNNING = set()


# ================= SAFE EDIT =================
async def safe_edit(msg: Message, text: str, **kwargs):
    try:
        await msg.edit_text(text, **kwargs)
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
        boot_phases = [
            "🌐 ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴘʀᴏɴᴏᴠᴀ ɴᴇᴛᴡᴏʀᴋ...",
            "⚙️ ʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ ᴅʀɪᴠᴇʀs...",
            "🛡️ sᴇᴄᴜʀɪɴɢ sᴇssɪᴏɴ...",
            "✅ sʏsᴛᴇᴍ ʀᴇᴀᴅʏ."
        ]

        for phase in boot_phases:
            await safe_edit(message, f"<code>{phase}</code>")
            await asyncio.sleep(0.5)

        header = f"🎼 **{BOT_NAME}**\n"
        line = "⎯" * 30 + "\n"

        welcome_text = f"ʜᴇʟʟᴏ {user_name}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴇʀᴀ ᴏꜰ ᴍᴜsɪᴄ."
        words = welcome_text.split()

        current = ""
        for word in words:
            current += word + " "
            await safe_edit(message, f"{header}{line}*“ {current}▎ ”*\n{line}")
            await asyncio.sleep(0.12)

        dashboard = (
            f"🎼 **{BOT_NAME}**\n"
            f"{line}"
            "●─────────── 𝟶𝟻:𝟸𝟶\n"
            "⇆   ◁   ❚❚   ▷   ↻\n"
            f"{line}"
            "👤 **ᴜsᴇʀ:** `ᴘʀᴇᴍɪᴜᴍ`\n"
            "🔊 **ǫᴜᴀʟɪᴛʏ:** `𝟸𝟺-ʙɪᴛ`\n"
            "📶 **ʟᴀᴛᴇɴᴄʏ:** `ᴜʟᴛʀᴀ ʟᴏᴡ`\n"
            f"{line}"
            "✨ **ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ**"
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

    # ===== SAVE USER + CHAT =====
    try:
        await add_user(user)
        await add_chat(message.chat)
    except Exception as e:
        print("START STATS FAIL:", e)

    user_name = user.mention

    try:
        await message.reply_sticker(MUSIC_STICKER)
    except Exception as e:
        print("[StartUI Sticker]", e)

    try:
        status_msg = await message.reply_text(
            "📶 `ɪɴɪᴛɪᴀʟɪᴢɪɴɢ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑪𝒐𝒓𝒆...`",
            quote=True
        )
    except Exception as e:
        print("[StartUI Init]", e)
        return

    await pronova_ultimate_animation(status_msg, user_name)
    
