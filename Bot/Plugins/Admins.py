from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Font import sc
from Bot.Database.Bans import is_banned, is_gbanned


# ================= ADMIN =================
async def is_admin(chat_id, user_id):
    if not user_id:
        return False

    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except:
        return False


# ================= BAN =================
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


# ================= SAFE VC =================
async def safe_vc_action(action, chat_id):
    try:
        return await action(chat_id)
    except Exception as e:
        print("VC Action Error:", e)
        return None


# ================= COMMON CHECK =================
async def admin_only(m):
    if await check_ban(m):
        return False

    if not m.from_user or not await is_admin(m.chat.id, m.from_user.id):
        await m.reply(sc("admins only"))
        return False

    return True


# ================= SKIP =================
@bot.on_message(filters.command("skip"))
async def skip(_, m):
    if not await admin_only(m):
        return

    await safe_vc_action(engine.vc.skip, m.chat.id)
    await m.reply(sc("song skipped by") + " " + m.from_user.mention)


# ================= STOP =================
@bot.on_message(filters.command(["stop", "end"]))
async def stop(_, m):
    if not await admin_only(m):
        return

    await safe_vc_action(engine.vc.stop, m.chat.id)
    await m.reply(sc("playback ended by") + " " + m.from_user.mention)


# ================= PAUSE =================
@bot.on_message(filters.command("pause"))
async def pause(_, m):
    if not await admin_only(m):
        return

    await safe_vc_action(engine.vc.pause, m.chat.id)
    await m.reply(sc("paused by") + " " + m.from_user.mention)


# ================= RESUME =================
@bot.on_message(filters.command("resume"))
async def resume(_, m):
    if not await admin_only(m):
        return

    await safe_vc_action(engine.vc.resume, m.chat.id)
    await m.reply(sc("resumed by") + " " + m.from_user.mention)


# ================= PREVIOUS =================
@bot.on_message(filters.command("previous"))
async def previous(_, m):
    if not await admin_only(m):
        return

    ok = await safe_vc_action(engine.vc.previous, m.chat.id)
    if not ok:
        return await m.reply(sc("no previous song"))

    await m.reply(sc("previous played by") + " " + m.from_user.mention)


# ================= QUEUE =================
@bot.on_message(filters.command("queue"))
async def queue(_, m):
    if not await admin_only(m):
        return

    try:
        q = engine.vc.player.queues.get(m.chat.id)
        if not q or not getattr(q, "items", None):
            return await m.reply(sc("queue empty"))

        text = sc("queue list") + "\n\n"

        for i, s in enumerate(q.items, 1):
            title = getattr(s, "title", "unknown")
            dur = getattr(s, "duration_sec", 0)
            text += f"{i}. {title} ({dur}s)\n"

        await m.reply(text)

    except Exception as e:
        print("Queue Error:", e)
        await m.reply(sc("unable to fetch queue"))
