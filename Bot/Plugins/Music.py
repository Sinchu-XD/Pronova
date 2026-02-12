from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Assistant import get_ass
from Bot.Helper.Font import sc

from Bot.Database.Songs import inc_song_play
from Bot.Database.Bans import is_banned, is_gbanned
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat


# ================= ADMIN CHECK =================
async def is_admin(chat_id, user_id):
    if not user_id:
        return False

    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )


# ================= BAN CHECK =================
async def check_ban(m):
    if not m.from_user:
        return True

    uid = m.from_user.id
    chat_id = m.chat.id

    if await is_gbanned(uid):
        await m.reply(sc("you are gbanned"))
        return True

    if await is_banned(chat_id, uid):
        await m.reply(sc("you are banned in this chat"))
        return True

    return False


# ================= SAFE DELETE =================
async def safe_delete(m):
    try:
        await m.delete()
    except:
        pass


# ================= PLAY LOGIC =================
async def handle_play(m, force=False):
    if await check_ban(m):
        return

    if not m.from_user:
        return

    uid = m.from_user.id
    chat_id = m.chat.id

    if force and not await is_admin(chat_id, uid):
        return await m.reply(sc("admins only"))

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
            return await m.reply(sc("download failed"))

        try:
            song, title = await engine.vc.play_file(
                chat_id,
                path,
                m.from_user.mention,
                reply=reply
            )
        except Exception as e:
            print("Play File Error:", e)
            return await m.reply(sc("unable to play audio"))

        if not song:
            return await m.reply(sc("unable to play audio"))

        # ===== SAVE STATS =====
        await inc_song_play(chat_id, title or query)

        print("TRY ADD USER", m.from_user.id)

        try:
            await add_user(m.from_user)
            await add_chat(chat_id)
            print("USER SUCCESS")
        except Exception as e:
            print("USER FAIL:", e)

        return

    # ================= QUERY =================
    if len(m.command) < 2:
        return await m.reply(sc("give song name"))

    query = m.text.split(None, 1)[1]

    try:
        song, title = await engine.vc.play(
            chat_id,
            query,
            m.from_user.mention
        )
    except Exception as e:
        print("Play Query Error:", e)
        return await m.reply(sc("unable to play song"))

    if not song:
        return await m.reply(sc("unable to play song"))

    # ===== SAVE STATS =====
        await inc_song_play(chat_id, title or query)

        print("TRY ADD USER", m.from_user.id)

        try:
            await add_user(m.from_user)
            await add_chat(chat_id)
            print("USER SUCCESS")
        except Exception as e:
            print("USER FAIL:", e)


# ================= PLAY =================
@bot.on_message(filters.command("play"))
async def play(_, m):
    await safe_delete(m)
    await handle_play(m, force=False)


# ================= PLAY FORCE =================
@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    await safe_delete(m)
    await handle_play(m, force=True)
    
