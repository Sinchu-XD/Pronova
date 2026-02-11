from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Assistant import get_ass
from Bot.Helper.Font import sc

# ===== DB =====
from Bot.Database.Songs import inc_song_play
from Bot.Database.Bans import is_banned, is_gbanned


# ───────── ADMIN CHECK ─────────
async def is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )


# ───────── BAN CHECK HELPER ─────────
async def check_ban(m):
    if not m.from_user:
        return True

    uid = m.from_user.id

    if await is_gbanned(uid):
        await m.reply(sc("you are gbanned"))
        return True

    if await is_banned(uid):
        await m.reply(sc("you are banned"))
        return True

    return False


# ───────── PLAY ─────────
@bot.on_message(filters.command("play"))
async def play(_, m):
    try:
        await m.delete()
    except:
        pass

    if await check_ban(m):
        return

    if not await get_ass(m.chat.id, m):
        return

    reply = m.reply_to_message

    # ===== REPLY AUDIO =====
    if reply and (reply.voice or reply.audio):
        path = await reply.download()

        try:
            song, title = await engine.vc.play_file(
                m.chat.id, path, m.from_user.mention, reply=reply
            )
        except Exception as e:
            print("Play Error:", e)
            return await m.reply(sc("unable to play audio"))

        if not song:
            return await m.reply(sc("unable to play audio"))

        await inc_song_play(m.chat.id, title or "Telegram Audio")
        return

    if len(m.command) < 2:
        return await m.reply(sc("usage play song name"))

    query = m.text.split(None, 1)[1]

    try:
        song, title = await engine.vc.play(
            m.chat.id, query, m.from_user.mention
        )
    except Exception as e:
        print("Play Error:", e)
        return await m.reply(sc("unable to play song"))

    if not song:
        return await m.reply(sc("unable to play song"))

    await inc_song_play(m.chat.id, title or query)


# ───────── PLAY FORCE (ADMINS ONLY) ─────────
@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    try:
        await m.delete()
    except:
        pass

    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    if not await get_ass(m.chat.id, m):
        return

    await engine.vc.stop(m.chat.id)

    reply = m.reply_to_message

    # ===== REPLY AUDIO =====
    if reply and (reply.voice or reply.audio):
        path = await reply.download()

        try:
            song, title = await engine.vc.play_file(
                m.chat.id, path, m.from_user.mention, reply=reply
            )
        except Exception as e:
            print("Force Play Error:", e)
            return await m.reply(sc("force play failed"))

        if not song:
            return await m.reply(sc("force play failed"))

        await inc_song_play(m.chat.id, title or "Telegram Audio")
        return

    if len(m.command) < 2:
        return await m.reply(sc("usage playforce song"))

    query = m.text.split(None, 1)[1]

    try:
        song, title = await engine.vc.play(
            m.chat.id, query, m.from_user.mention
        )
    except Exception as e:
        print("Force Play Error:", e)
        return await m.reply(sc("force play failed"))

    if not song:
        return await m.reply(sc("force play failed"))

    await inc_song_play(m.chat.id, title or query)
    
