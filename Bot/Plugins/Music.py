from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Assistant import get_ass
from Bot.Helper.Font import sc
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
        text, ent = add_premium(sc("you are gbanned"))
        await m.reply(text, entities=ent)
        return True

    if await is_banned(chat_id, uid):
        text, ent = add_premium(sc("you are banned in this chat"))
        await m.reply(text, entities=ent)
        return True

    return False


# ================= SAFE DELETE =================
async def safe_delete(m):
    try:
        await m.delete()
    except:
        pass


# ================= REGISTER USAGE =================
async def register_usage(m):
    if not m.from_user:
        return

    try:
        await add_user(m.from_user)
        await add_chat(m.chat)
    except Exception as e:
        print("Usage Register Error:", e)


# ================= PLAY LOGIC =================
async def handle_play(m, force=False):
    if await check_ban(m):
        return

    if not m.from_user:
        return

    uid = m.from_user.id
    chat_id = m.chat.id

    if force and not await is_admin(chat_id, uid):
        text, ent = add_premium(sc("admins only"))
        return await m.reply(text, entities=ent)

    if not await get_ass(chat_id, m):
        return

    if force:
        try:
            await engine.vc.stop(chat_id)
        except Exception as e:
            print("VC Stop Error:", e)

    reply = m.reply_to_message

    # ================= AUDIO =================
    if reply and (reply.voice or reply.audio):
        try:
            path = await reply.download()
        except Exception as e:
            print("Download Error:", e)
            text, ent = add_premium(sc("download failed"))
            return await m.reply(text, entities=ent)

        try:
            song, title = await engine.vc.play_file(
                chat_id,
                path,
                m.from_user.mention,
                reply=reply
            )
        except Exception as e:
            print("Play File Error:", e)
            text, ent = add_premium(sc("unable to play audio"))
            return await m.reply(text, entities=ent)

        if not song:
            text, ent = add_premium(sc("unable to play audio"))
            return await m.reply(text, entities=ent)

        await inc_song_play(chat_id, title)
        return

    # ================= QUERY =================
    if len(m.command) < 2:
        text, ent = add_premium(sc("give song name"))
        return await m.reply(text, entities=ent)

    query = m.text.split(None, 1)[1]

    try:
        song, title = await engine.vc.play(
            chat_id,
            query,
            m.from_user.mention
        )
    except Exception as e:
        print("Play Query Error:", e)
        text, ent = add_premium(sc("unable to play song"))
        return await m.reply(text, entities=ent)

    if not song:
        text, ent = add_premium(sc("unable to play song"))
        return await m.reply(text, entities=ent)

    await inc_song_play(chat_id, title or query)


# ================= PLAY =================
@bot.on_message(filters.command("play"))
async def play(_, m):
    await safe_delete(m)
    await register_usage(m)
    await handle_play(m, force=False)


# ================= PLAY FORCE =================
@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    await safe_delete(m)
    await register_usage(m)
    await handle_play(m, force=True)
    
