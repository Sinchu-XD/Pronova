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


# ───────── PLAY ─────────
@bot.on_message(filters.command("play"))
async def play(_, m):
    try:
        await m.delete()
    except:
        pass

    # ===== BAN CHECK =====
    uid = m.from_user.id
    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await get_ass(m.chat.id, m):
        return

    reply = m.reply_to_message

    # ===== REPLY AUDIO =====
    if reply and (reply.voice or reply.audio):
        path = await reply.download()
        song, title = await engine.vc.play_file(
            m.chat.id, path, m.from_user.mention, reply=reply
        )

        if not song:
            return await m.reply(sc("unable to play audio"))

        # ===== SUCCESS → COUNT =====
        await inc_song_play(m.chat.id, title or "Telegram Audio")
        return

    if len(m.command) < 2:
        return await m.reply(sc("usage play song name"))

    query = m.text.split(None, 1)[1]
    song, title = await engine.vc.play(
        m.chat.id, query, m.from_user.mention
    )

    if not song:
        return await m.reply(sc("unable to play song"))

    # ===== SUCCESS → COUNT =====
    await inc_song_play(m.chat.id, title or query)


# ───────── PLAY FORCE (ADMINS ONLY) ─────────
@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    try:
        await m.delete()
    except:
        pass

    # ===== BAN CHECK =====
    uid = m.from_user.id
    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    if not await get_ass(m.chat.id, m):
        return

    await engine.vc.stop(m.chat.id)

    reply = m.reply_to_message

    # ===== REPLY AUDIO =====
    if reply and (reply.voice or reply.audio):
        path = await reply.download()
        song, title = await engine.vc.play_file(
            m.chat.id, path, m.from_user.mention, reply=reply
        )

        if not song:
            return await m.reply(sc("force play failed"))

        # ===== SUCCESS → COUNT =====
        await inc_song_play(m.chat.id, title or "Telegram Audio")
        return

    if len(m.command) < 2:
        return await m.reply(sc("usage playforce song"))

    query = m.text.split(None, 1)[1]
    song, title = await engine.vc.play(
        m.chat.id, query, m.from_user.mention
    )

    if not song:
        return await m.reply(sc("force play failed"))

    # ===== SUCCESS → COUNT =====
    await inc_song_play(m.chat.id, title or query)
    
