import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# --- ꜱᴇᴛᴛɪɴɢꜱ ---
BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕🌷"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"

async def pronova_ultimate_animation(message: Message, user_name: str):
    """ᴇʟɪᴛᴇ ʙᴏᴏᴛ-ᴜᴘ sᴇǫᴜᴇɴᴄᴇ"""
    
    # Phase 1: High-Speed System Check
    boot_phases = [
        "🌐 ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴘʀᴏɴᴏᴠᴀ ɴᴇᴛᴡᴏʀᴋ...",
        "⚙️ ʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ ᴅʀɪᴠᴇʀs [ᴠ8.2]...",
        "🛡️ sᴇᴄᴜʀɪɴɢ sᴇssɪᴏɴ ᴇɴᴅ-ᴛᴏ-ᴇɴᴅ...",
        "✅ sʏsᴛᴇᴍ ʀᴇᴀᴅʏ. ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ."
    ]
    
    for phase in boot_phases:
        await message.edit_text(f"<code>{phase}</code>")
        await asyncio.sleep(0.5)

    # Phase 2: The "Aura" Reveal (Small Caps)
    header = f"🎼 **{BOT_NAME}**\n"
    line = "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    
    welcome_text = (
        f"ʜᴇʟʟᴏ {user_name}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴇʀᴀ ᴏꜰ ᴍᴜsɪᴄ ᴅᴇʟɪᴠᴇʀʏ. "
        "ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ᴅᴇᴘᴛʜ ᴏꜰ sᴏᴜɴᴅ ᴡɪᴛʜ ᴘʀᴏɴᴏᴠᴀ's ʟᴏssʟᴇss ᴛᴇᴄʜɴᴏʟᴏɢʏ."
    )
    
    # Word-by-word reveal for maximum smoothness
    words = welcome_text.split()
    current_text = ""
    for word in words:
        current_text += word + " "
        await message.edit_text(f"{header}{line}*“ {current_text}▎ ”*\n{line}")
        await asyncio.sleep(0.12)

    # Final Dashboard (Small Caps UI)
    dashboard = (
        f"🎼 **{BOT_NAME}**\n"
        f"{line}"
        "●─────────── 𝟶𝟻:𝟸𝟶\n"
        "⇆   ㅤ◁   ㅤ❚❚   ㅤ▷   ㅤ↻\n"
        f"{line}"
        "👤 **ᴜsᴇʀ:** `ᴘʀᴇᴍɪᴜᴍ ɢᴏʟᴅ`\n"
        "🔊 **ᴏᴜᴛᴘᴜᴛ:** `𝟸𝟺-ʙɪᴛ / 𝟷𝟿𝟸ᴋʜᴢ`\n"
        "📶 **ʟᴀᴛᴇɴᴄʏ:** `𝟶.𝟶𝟶𝟷ᴍs`\n"
        f"{line}"
        "✨ **ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ ʏᴏᴜʀ ᴊᴏᴜʀɴᴇʏ**"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(" ᴀᴅᴅ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 ᴛᴏ ɢʀᴏᴜᴘ ", url="https://t.me/yourbot?startgroup=true")],
        [
            InlineKeyboardButton("🔍 sᴇᴀʀᴄʜ", switch_inline_query_current_chat=""),
            InlineKeyboardButton("🏆 ᴛᴏᴘ ᴄʜᴀʀᴛs", callback_data="charts")
        ],
        [
            InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢs", callback_data="settings"),
            InlineKeyboardButton("📜 ᴘʟᴀʏʟɪsᴛs", callback_data="playlists")
        ],
        [InlineKeyboardButton("👑 ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Her4Eva")]
    ])

    await message.edit_text(dashboard, reply_markup=buttons)

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    # User's first name for personalization
    user_name = message.from_user.first_name
    
    # 1. Premium Sticker Entry
    await message.reply_sticker(MUSIC_STICKER)
    
    # 2. Initializing Message
    status_msg = await message.reply_text("📶 `ɪɴɪᴛɪᴀʟɪᴢɪɴɢ 𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕 ᴄᴏʀᴇ...`", quote=True)
    
    # 3. Start Animation
    await pronova_ultimate_animation(status_msg, user_name)
