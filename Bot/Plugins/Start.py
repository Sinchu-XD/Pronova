import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot import bot


BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕🌷"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"


# ==========================
# SMART SAFE EDIT
# ==========================
_last_text_cache = {}


async def safe_edit(msg: Message, text: str, **kwargs):
    """
    Smart edit:
    - skip same text
    - flood safe
    - deleted message safe
    """
    key = (msg.chat.id, msg.id)

    if _last_text_cache.get(key) == text:
        return

    try:
        await msg.edit_text(text, **kwargs)
        _last_text_cache[key] = text

    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" in str(e):
            return
        print("[StartUI:Edit]", e)


# ==========================
# ULTIMATE ANIMATION
# ==========================
async def pronova_ultimate_animation(message: Message, user_name: str):
    print("[StartUI] animation start")

    # Phase 1
    boot_phases = [
        "🌐 ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴘʀᴏɴᴏᴠᴀ ɴᴇᴛᴡᴏʀᴋ...",
        "⚙️ ʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ ᴅʀɪᴠᴇʀs [ᴠ8.2]...",
        "🛡️ sᴇᴄᴜʀɪɴɢ sᴇssɪᴏɴ ᴇɴᴅ-ᴛᴏ-ᴇɴᴅ...",
        "✅ sʏsᴛᴇᴍ ʀᴇᴀᴅʏ. ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ."
    ]

    for phase in boot_phases:
        await safe_edit(message, f"<code>{phase}</code>")
        await asyncio.sleep(0.5)

    # Phase 2
    header = f"🎼 **{BOT_NAME}**\n"
    line = "⎯" * 30 + "\n"

    welcome_text = (
        f"ʜᴇʟʟᴏ {user_name}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴇʀᴀ ᴏꜰ ᴍᴜsɪᴄ ᴅᴇʟɪᴠᴇʀʏ. "
        "ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ᴅᴇᴘᴛʜ ᴏꜰ sᴏᴜɴᴅ."
    )

    words = welcome_text.split()
    current = ""

    for word in words:
        current += word + " "
        await safe_edit(message, f"{header}{line}*“ {current}▎ ”*\n{line}")
        await asyncio.sleep(0.12)

    # Final
    dashboard = (
        f"🎼 **{BOT_NAME}**\n"
        f"{line}"
        "●─────────── 𝟶𝟻:𝟸𝟶\n"
        "⇆   ㅤ◁   ㅤ❚❚   ㅤ▷   ㅤ↻\n"
        f"{line}"
        "👤 **ᴜsᴇʀ:** `ᴘʀᴇᴍɪᴜᴍ`\n"
        "🔊 **ǫᴜᴀʟɪᴛʏ:** `𝟸𝟺-ʙɪᴛ`\n"
        "📶 **ʟᴀᴛᴇɴᴄʏ:** `ᴜʟᴛʀᴀ ʟᴏᴡ`\n"
        f"{line}"
        "✨ **ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ**"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(" ᴀᴅᴅ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 ᴛᴏ ɢʀᴏᴜᴘ ", url="https://t.me/ProNovaMusicBot?startgroup=true")],
        [InlineKeyboardButton("👑 ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Her4Eva")]
    ])

    await safe_edit(message, dashboard, reply_markup=buttons)

    print("[StartUI] animation end")


# ==========================
# START
# ==========================
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    print("[StartUI] /start")

    user_name = message.from_user.mention

    try:
        await message.reply_sticker(MUSIC_STICKER)
    except Exception as e:
        print("[StartUI:Sticker]", e)

    try:
        status_msg = await message.reply_text(
            "📶 `ɪɴɪᴛɪᴀʟɪᴢɪɴɢ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑪𝒐𝒓𝒆...`",
            quote=True
        )
    except Exception as e:
        print("[StartUI:InitMsg]", e)
        return

    await pronova_ultimate_animation(status_msg, user_name)
