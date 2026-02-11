import time
from pyrogram import filters
from pyrogram.types import Message

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.Afk import set_afk_db, get_afk, remove_afk_db


# anti spam
LAST_REPLY = {}


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
    user = message.from_user
    if not user:
        return

    reason = "Away"
    if len(message.command) > 1:
        reason = " ".join(message.command[1:])

    await set_afk_db(user.id, reason)

    await message.reply_text(
        sc(f"""
AFK Enabled

{user.mention}
Reason : {reason}

I will inform anyone who mentions you.
""")
    )


# ================= AUTO REMOVE =================
@bot.on_message(filters.all & ~filters.command("afk"))
async def auto_remove_afk(_, message: Message):
    user = message.from_user
    if not user:
        return

    data = await get_afk(user.id)
    if not data:
        return

    since = data["since"].timestamp()
    duration = format_time(time.time() - since)

    await remove_afk_db(user.id)

    await message.reply_text(
        sc(f"""
Welcome Back

{user.mention}
Away for : {duration}
""")
    )


# ================= WATCH =================
@bot.on_message(filters.group)
async def afk_watcher(_, message: Message):
    if not message.from_user:
        return

    targets = []

    # reply
    if message.reply_to_message and message.reply_to_message.from_user:
        targets.append(message.reply_to_message.from_user)

    # mentions
    if message.mentions:
        targets.extend(message.mentions)

    for user in targets:
        data = await get_afk(user.id)
        if not data:
            continue

        key = (message.chat.id, user.id)
        last = LAST_REPLY.get(key, 0)

        if time.time() - last < 15:
            continue

        LAST_REPLY[key] = time.time()

        since = data["since"].timestamp()
        duration = format_time(time.time() - since)

        await message.reply_text(
            sc(f"""
User is AFK

{user.mention}
Last Seen : {duration}
Reason : {data['reason']}
""")
        )
        
