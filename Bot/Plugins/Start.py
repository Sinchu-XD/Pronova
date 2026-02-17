import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Bot import bot
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat


BOT_NAME = "𝑷𝒓𝒐𝒏𝒐𝒗𝒂 𝑴𝒖𝒔𝒊𝒄 𝑩𝒐𝒕🌷"
MUSIC_STICKER = "CAACAgUAAx0CZzxBYgABB2zoaYjxDe3E6k4Spe_lmG-wfKUjdrYAAm8VAAKaqulXWtKxQoF0Y_UeBA"


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
    
from pyrogram import filters

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.Users import total_users
from Bot.Database.Chats import total_chats
from Bot.Database.Songs import most_played
from Bot.Database.Ranking import top_groups, top_users
from Bot.Database.Stats import get_lifetime, sum_range
from Bot.Database.Bans import total_banned
from Bot.Database.Core import db


SUDO_USERS = [7952773964]

USER_CACHE = {}
CHAT_CACHE = {}


@bot.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats(_, m):
    msg = await m.reply(sc("fetching analytics..."))

    try:
        users = await total_users()
        chats = await total_chats()
        songs = await get_lifetime("songs")
        commands = await get_lifetime("commands")

        banned = await total_banned()
        gbanned = await db.gbanned.count_documents({})

        weekly_users = await sum_range(7, "users")
        monthly_users = await sum_range(30, "users")

        tg = await top_groups(3)
        tu = await top_users(3)
        mp = await most_played(3)

    except Exception as e:
        print("Stats Fetch Error:", e)
        return await msg.edit(sc("failed to fetch stats"))

    # ================= HEADER =================
    text = f"📊 {sc('bot analytics')}\n\n"

    # ================= BASIC =================
    text += f"{sc('users')} : {users}\n"
    text += f"{sc('chats')} : {chats}\n"
    text += f"{sc('songs')} : {songs}\n"
    text += f"{sc('commands')} : {commands}\n\n"

    # ================= BANS =================
    text += f"{sc('banned (groups)')} : {banned}\n"
    text += f"{sc('gbanned (global)')} : {gbanned}\n\n"

    # ================= GROWTH =================
    text += f"📈 {sc('growth')}\n"
    text += f"7 {sc('days')} : {weekly_users}\n"
    text += f"30 {sc('days')} : {monthly_users}\n\n"

    # ================= TOP GROUPS =================
    text += f"🏆 {sc('top groups')}\n"

    if tg:
        for i, (cid, s) in enumerate(tg, 1):
            try:
                cid = int(cid)

                if cid in CHAT_CACHE:
                    name = CHAT_CACHE[cid]
                else:
                    chat = await bot.get_chat(cid)
                    name = chat.title
                    CHAT_CACHE[cid] = name

            except:
                name = cid

            text += f"{i}. {name} → {s}\n"
    else:
        text += f"{sc('no data')}\n"

    # ================= TOP USERS =================
    text += f"\n👤 {sc('top users')}\n"

    if tu:
        for i, (uid, c) in enumerate(tu, 1):
            try:
                uid = int(uid)

                if uid in USER_CACHE:
                    mention = USER_CACHE[uid]
                else:
                    user = await bot.get_users(uid)
                    mention = user.mention
                    USER_CACHE[uid] = mention

            except:
                mention = uid

            text += f"{i}. {mention} → {c}\n"
    else:
        text += f"{sc('no data')}\n"

    # ================= MOST PLAYED =================
    text += f"\n🎧 {sc('most played')}\n"

    if mp:
        for i, (name, c) in enumerate(mp, 1):
            text += f"{i}. {name} → {c}\n"
    else:
        text += f"{sc('no data')}\n"

    try:
        await msg.edit(text)
    except Exception as e:
        print("Stats Edit Error:", e)
        
