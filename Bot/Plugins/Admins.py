from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Font import sc
from Bot.Helper.Emoji import add_premium
from Bot.Database.Bans import is_banned, is_gbanned


# ================= ADMIN CHECK =================
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


# ================= ADMIN ONLY =================
async def admin_only(m):
    if await check_ban(m):
        return False

    if not m.from_user or not await is_admin(m.chat.id, m.from_user.id):
        text, ent = add_premium(sc("admins only"))
        await m.reply(text, entities=ent)
        return False

    return True


# ================= SAFE VC =================
async def safe(action, chat_id):
    try:
        return await action(chat_id)
    except Exception as e:
        print("VC Error:", e)
        return None


# ================= SKIP =================
@bot.on_message(filters.command("skip"))
async def skip(_, m):
    if not await admin_only(m):
        return

    await safe(engine.vc.skip, m.chat.id)

    text, ent = add_premium(sc("song skipped by") + " " + m.from_user.mention)
    await m.reply(text, entities=ent)


# ================= STOP =================
@bot.on_message(filters.command(["stop", "end"]))
async def stop(_, m):
    if not await admin_only(m):
        return

    await safe(engine.vc.stop, m.chat.id)

    text, ent = add_premium(sc("playback ended by") + " " + m.from_user.mention)
    await m.reply(text, entities=ent)


# ================= PAUSE =================
@bot.on_message(filters.command("pause"))
async def pause(_, m):
    if not await admin_only(m):
        return

    await safe(engine.vc.pause, m.chat.id)

    text, ent = add_premium(sc("paused by") + " " + m.from_user.mention)
    await m.reply(text, entities=ent)


# ================= RESUME =================
@bot.on_message(filters.command("resume"))
async def resume(_, m):
    if not await admin_only(m):
        return

    await safe(engine.vc.resume, m.chat.id)

    text, ent = add_premium(sc("resumed by") + " " + m.from_user.mention)
    await m.reply(text, entities=ent)


# ================= PREVIOUS =================
@bot.on_message(filters.command("previous"))
async def previous(_, m):
    if not await admin_only(m):
        return

    ok = await safe(engine.vc.previous, m.chat.id)

    if not ok:
        text, ent = add_premium(sc("no previous song"))
        return await m.reply(text, entities=ent)

    text, ent = add_premium(sc("previous played by") + " " + m.from_user.mention)
    await m.reply(text, entities=ent)


# ================= QUEUE =================
@bot.on_message(filters.command("queue"))
async def queue(_, m):
    if not await admin_only(m):
        return

    try:
        q = engine.vc.player.queues.get(m.chat.id)

        if not q or not getattr(q, "items", None):
            text, ent = add_premium(sc("queue empty"))
            return await m.reply(text, entities=ent)

        text = sc("queue list") + "\n\n"

        for i, s in enumerate(q.items, 1):
            title = getattr(s, "title", "unknown")
            dur = getattr(s, "duration_sec", 0)
            text += f"{i}. {title} ({dur}s)\n"

        text, ent = add_premium(text.strip())
        await m.reply(text, entities=ent)

    except Exception as e:
        print("Queue Error:", e)
        text, ent = add_premium(sc("unable to fetch queue"))
        await m.reply(text, entities=ent)
        
