from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Font import sc

# ===== DB =====
from Bot.Database.bans import is_banned, is_gbanned
from Bot.Database.stats import inc_lifetime, inc_daily


# helper
async def count_command():
    await inc_lifetime("commands")
    await inc_daily("commands")


# ───────── ADMIN CHECK ─────────
async def is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )


# ───────── SKIP ─────────
@bot.on_message(filters.command("skip"))
async def skip(_, m):
    uid = m.from_user.id

    # ===== BAN CHECK =====
    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, uid):
        return await m.reply(sc("admins only"))

    await count_command()

    await engine.vc.skip(m.chat.id)
    await m.reply(sc("song skipped by") + " " + m.from_user.mention)


# ───────── STOP ─────────
@bot.on_message(filters.command(["stop", "end"]))
async def stop(_, m):
    uid = m.from_user.id

    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, uid):
        return await m.reply(sc("admins only"))

    await count_command()

    await engine.vc.stop(m.chat.id)
    await m.reply(sc("playback ended by") + " " + m.from_user.mention)


# ───────── PAUSE ─────────
@bot.on_message(filters.command("pause"))
async def pause(_, m):
    uid = m.from_user.id

    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, uid):
        return await m.reply(sc("admins only"))

    await count_command()

    await engine.vc.pause(m.chat.id)
    await m.reply(sc("paused by") + " " + m.from_user.mention)


# ───────── RESUME ─────────
@bot.on_message(filters.command("resume"))
async def resume(_, m):
    uid = m.from_user.id

    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, uid):
        return await m.reply(sc("admins only"))

    await count_command()

    await engine.vc.resume(m.chat.id)
    await m.reply(sc("resumed by") + " " + m.from_user.mention)


# ───────── PREVIOUS ─────────
@bot.on_message(filters.command("previous"))
async def previous(_, m):
    uid = m.from_user.id

    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, uid):
        return await m.reply(sc("admins only"))

    await count_command()

    ok = await engine.vc.previous(m.chat.id)
    if not ok:
        return await m.reply(sc("no previous song"))

    await m.reply(sc("previous played by") + " " + m.from_user.mention)


# ───────── QUEUE ─────────
@bot.on_message(filters.command("queue"))
async def queue(_, m):
    uid = m.from_user.id

    if await is_gbanned(uid):
        return await m.reply("🚫 You are gbanned.")
    if await is_banned(uid):
        return await m.reply("🚫 You are banned.")

    if not await is_admin(m.chat.id, uid):
        return await m.reply(sc("admins only"))

    await count_command()

    q = engine.vc.player.queues.get(m.chat.id)
    if not q or not q.items:
        return await m.reply(sc("queue empty"))

    text = sc("queue list") + "\n\n"

    for i, s in enumerate(q.items, 1):
        text += f"{i}. {s.title} ({s.duration_sec}s)\n"

    await m.reply(text)
    
