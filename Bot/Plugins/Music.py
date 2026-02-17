from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Assistant import get_ass
from Bot.Helper.Emoji import add_premium

from Bot.Database.Songs import inc_song_play
from Bot.Database.Bans import is_banned, is_gbanned
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat


# ================= ADMIN CHECK =================
async def is_admin(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except:
        return False


# ================= BAN CHECK =================
async def check_ban(m):
    if not m.from_user:
        return True

    uid = m.from_user.id
    chat_id = m.chat.id

    if await is_gbanned(uid):
        text = add_premium("You are gbanned")
        await m.reply(text, parse_mode="html")
        return True

    if await is_banned(chat_id, uid):
        text = add_premium("You are banned in this chat")
        await m.reply(text, parse_mode="html")
        return True

    return False


# ================= SAFE DELETE =================
async def safe_delete(m):
    try:
        await m.delete()
    except:
        pass


# ================= REGISTER =================
async def register_usage(m):
    if not m.from_user:
        return
    try:
        await add_user(m.from_user)
        await add_chat(m.chat)
    except:
        pass


# ================= PLAY LOGIC =================
async def handle_play(m, force=False):

    if await check_ban(m):
        return

    if not m.from_user:
        return

    chat_id = m.chat.id
    uid = m.from_user.id

    if force and not await is_admin(chat_id, uid):
        text = add_premium("Admins only")
        return await m.reply(text, parse_mode="html")

    if not await get_ass(chat_id, m):
        return

    if force:
        try:
            await engine.vc.stop(chat_id)
        except:
            pass

    reply = m.reply_to_message

    # ================= AUDIO FILE =================
    if reply and (reply.voice or reply.audio):
        try:
            path = await reply.download()
        except:
            text = add_premium("Download failed")
            return await m.reply(text, parse_mode="html")

        try:
            song, title = await engine.vc.play_file(
                chat_id,
                path,
                m.from_user.mention,
                reply=reply
            )
        except:
            text = add_premium("Unable to play audio")
            return await m.reply(text, parse_mode="html")

        if not song:
            text = add_premium("Unable to play audio")
            return await m.reply(text, parse_mode="html")

        await inc_song_play(chat_id, title)

        text = add_premium(f"Now Playing: {title}")
        return await m.reply(text, parse_mode="html")

    # ================= TEXT QUERY =================
    if len(m.command) < 2:
        text = add_premium("Give song name")
        return await m.reply(text, parse_mode="html")

    query = m.text.split(None, 1)[1]

    try:
        song, title = await engine.vc.play(
            chat_id,
            query,
            m.from_user.mention
        )
    except:
        text = add_premium("Unable to play song")
        return await m.reply(text, parse_mode="html")

    if not song:
        text = add_premium("Unable to play song")
        return await m.reply(text, parse_mode="html")

    await inc_song_play(chat_id, title or query)

    text = add_premium(f"Now Playing: {title or query}")
    await m.reply(text, parse_mode="html")


# ================= COMMANDS =================
@bot.on_message(filters.command("play"))
async def play(_, m):
    await safe_delete(m)
    await register_usage(m)
    await handle_play(m, force=False)


@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    await safe_delete(m)
    await register_usage(m)
    await handle_play(m, force=True)


# ================= DEBUG =================
@bot.on_message(filters.command("debug"))
async def debug(_, message):
    text = add_premium("Hello World")
    await message.reply(text, parse_mode="html")
