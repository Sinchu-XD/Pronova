import time
from pyrogram import filters
from pyrogram.types import Message

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.Afk import set_afk_db, get_afk, remove_afk_db


# anti spam
LAST_REPLY = {}
SPAM_COOLDOWN = 15
CACHE_LIMIT = 10000


# ================= TIME FORMAT =================
def format_time(seconds: int):
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {sec}s"
    return f"{sec}s"


# ================= SET AFK =================
@bot.on_message(filters.command("afk"))
async def set_afk(_, message: Message):
    user = message.from_user.mention
    if not user:
        return

    reason = "Away"
    if len(message.command) > 1:
        reason = " ".join(message.command[1:])

    await set_afk_db(user.id, reason)

    await message.reply_text(
        sc(f"""
AFK Enabled

{user}
Reason : {reason}

I will inform anyone who mentions you.
""")
    )


# ================= AUTO REMOVE =================
@bot.on_message(filters.all & ~filters.command("afk"))
async def auto_remove_afk(_, message: Message):
    user = message.from_user.mention
    if not user:
        return

    data = await get_afk(user.id)
    if not data:
        return

    try:
        since = data["since"].timestamp()
    except Exception:
        since = time.time()

    duration = format_time(time.time() - since)

    await remove_afk_db(user.id)

    await message.reply_text(
        sc(f"""
Welcome Back

{user}
Away for : {duration}
""")
    )


# ================= WATCH =================
@bot.on_message(filters.group)
async def afk_watcher(_, message: Message):
    if not message.from_user:
        return

    targets = {}

    # reply
    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        targets[u.id] = u

    # mentions
    if message.mentions:
        for u in message.mentions:
            targets[u.id] = u

    for uid, user in targets.items():
        if user.is_bot:
            continue

        data = await get_afk(uid)
        if not data:
            continue

        key = (message.chat.id, uid)
        last = LAST_REPLY.get(key, 0)

        if time.time() - last < SPAM_COOLDOWN:
            continue

        LAST_REPLY[key] = time.time()

        # memory control
        if len(LAST_REPLY) > CACHE_LIMIT:
            LAST_REPLY.clear()

        try:
            since = data["since"].timestamp()
        except Exception:
            since = time.time()

        duration = format_time(time.time() - since)

        await message.reply_text(
            sc(f"""
User is AFK

{user.mention}
Last Seen : {duration}
Reason : {data.get('reason', 'Away')}
""")
        )
        
