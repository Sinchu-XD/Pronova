
import time
from pyrogram import filters
from pyrogram.types import Message

from Bot import bot
from Bot.Helper.Font import sc
from Bot.Helper.Emoji import add_premium
from Bot.Database.Afk import set_afk_db, get_afk, remove_afk_db


LAST_REPLY = {}
SPAM_COOLDOWN = 15
CACHE_LIMIT = 10000


# ================= TIME FORMAT =================
def format_time(seconds: int):
    try:
        seconds = int(seconds)
    except:
        return "0s"

    minutes, sec = divmod(seconds, 60)
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
    if not user or user.is_bot:
        return

    reason = "Away"
    if len(message.command) > 1:
        reason = " ".join(message.command[1:])

    await set_afk_db(user, reason)

    text = sc(
        f"afk enabled\n\n"
        f"reason : {reason}\n\n"
        f"i will inform anyone who mentions you."
    )

    text = f"{text}\n\n{user.mention}"
    text, ent = add_premium(text)

    await message.reply_text(text, entities=ent)


# ================= AUTO REMOVE =================
@bot.on_message(filters.all & ~filters.command("afk"))
async def auto_remove_afk(_, message: Message):
    user = message.from_user
    if not user or user.is_bot:
        return

    data = await get_afk(user)
    if not data:
        return

    try:
        since = data["since"].timestamp()
    except:
        since = time.time()

    duration = format_time(time.time() - since)

    await remove_afk_db(user)

    text = sc(
        f"welcome back\n\n"
        f"away for : {duration}"
    )

    text = f"{text}\n\n{user.mention}"
    text, ent = add_premium(text)

    await message.reply_text(text, entities=ent)


# ================= WATCH =================
@bot.on_message(filters.group)
async def afk_watcher(_, message: Message):
    if not message.from_user or message.from_user.is_bot:
        return

    targets = {}

    # Reply target
    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        targets[u.id] = u

    # Mention targets
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

        if len(LAST_REPLY) > CACHE_LIMIT:
            LAST_REPLY.clear()

        try:
            since = data["since"].timestamp()
        except:
            since = time.time()

        duration = format_time(time.time() - since)

        text = sc(
            f"user is afk\n\n"
            f"last seen : {duration}\n"
            f"reason : {data.get('reason', 'Away')}"
        )

        text = f"{text}\n\n{user.mention}"
        text, ent = add_premium(text)

        await message.reply_text(text, entities=ent)
        
