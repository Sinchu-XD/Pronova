from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Font import sc

# ===== DB =====
from Bot.Database.Bans import is_banned, is_gbanned


# ───────── ADMIN CHECK ─────────
async def is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )


# helper
async def check_ban(m):
    uid = m.from_user.id
    if await is_gbanned(uid):
        await m.reply("🚫 You are gbanned.")
        return True
    if await is_banned(uid):
        await m.reply("🚫 You are banned.")
        return True
    return False


# ───────── SKIP ─────────
@bot.on_message(filters.command("skip"))
async def skip(_, m):
    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    await engine.vc.skip(m.chat.id)
    await m.reply(sc("song skipped by") + " " + m.from_user.mention)


# ───────── STOP ─────────
@bot.on_message(filters.command(["stop", "end"]))
async def stop(_, m):
    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    await engine.vc.stop(m.chat.id)
    await m.reply(sc("playback ended by") + " " + m.from_user.mention)


# ───────── PAUSE ─────────
@bot.on_message(filters.command("pause"))
async def pause(_, m):
    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    await engine.vc.pause(m.chat.id)
    await m.reply(sc("paused by") + " " + m.from_user.mention)


# ───────── RESUME ─────────
@bot.on_message(filters.command("resume"))
async def resume(_, m):
    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    await engine.vc.resume(m.chat.id)
    await m.reply(sc("resumed by") + " " + m.from_user.mention)


# ───────── PREVIOUS ─────────
@bot.on_message(filters.command("previous"))
async def previous(_, m):
    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    ok = await engine.vc.previous(m.chat.id)
    if not ok:
        return await m.reply(sc("no previous song"))

    await m.reply(sc("previous played by") + " " + m.from_user.mention)


# ───────── QUEUE ─────────
@bot.on_message(filters.command("queue"))
async def queue(_, m):
    if await check_ban(m):
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    q = engine.vc.player.queues.get(m.chat.id)
    if not q or not q.items:
        return await m.reply(sc("queue empty"))

    text = sc("queue list") + "\n\n"

    for i, s in enumerate(q.items, 1):
        text += f"{i}. {s.title} ({s.duration_sec}s)\n"

    await m.reply(text)
    
