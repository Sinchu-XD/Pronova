from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Assistant import get_ass
from Bot.Helper.Font import sc


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

    if not await get_ass(m.chat.id, m):
        return

    reply = m.reply_to_message

    if reply and (reply.voice or reply.audio):
        path = await reply.download()
        song, _ = await engine.vc.play_file(
            m.chat.id, path, m.from_user.mention, reply=reply
        )
        if not song:
            await m.reply(sc("unable to play audio"))
        return

    if len(m.command) < 2:
        return await m.reply(sc("usage play song name"))

    query = m.text.split(None, 1)[1]
    song, _ = await engine.vc.play(m.chat.id, query, m.from_user.mention)

    if not song:
        await m.reply(sc("unable to play song"))


# ───────── PLAY FORCE (ADMINS ONLY) ─────────
@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    try:
        await m.delete()
    except:
        pass

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    if not await get_ass(m.chat.id, m):
        return

    await engine.vc.stop(m.chat.id)

    reply = m.reply_to_message

    if reply and (reply.voice or reply.audio):
        path = await reply.download()
        song, _ = await engine.vc.play_file(
            m.chat.id, path, m.from_user.mention, reply=reply
        )
        if not song:
            await m.reply(sc("force play failed"))
        return

    if len(m.command) < 2:
        return await m.reply(sc("usage playforce song"))

    query = m.text.split(None, 1)[1]
    await engine.vc.play(m.chat.id, query, m.from_user.mention)
    
