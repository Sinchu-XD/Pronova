import time
import random
from pyrogram import filters, enums
from pyrogram.types import Message, MessageEntity

from Bot import bot, CUSTOM_EMOJI_IDS
from Bot.Helper.Font import sc
from Bot.Database.Afk import set_afk_db, get_afk, remove_afk_db


LAST_REPLY = {}
SPAM_COOLDOWN = 15
CACHE_LIMIT = 10000


# ================= EMOJI HELPER =================
def add_random_emoji(text: str):
    emoji_id = random.choice(CUSTOM_EMOJI_IDS)

    text = text + " ❤️"

    entity = MessageEntity(
        type=enums.MessageEntityType.CUSTOM_EMOJI,
        offset=len(text) - 1,
        length=1,
        custom_emoji_id=emoji_id
    )

    return text, [entity]


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

    text = sc(f"""
AFK Enabled

Reason : {reason}

I will inform anyone who mentions you.
""")

    text = f"{text}\n\n{user.mention}"
    text, ent = add_random_emoji(text)

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

    text = sc(f"""
Welcome Back

Away for : {duration}
""")

    text = f"{text}\n\n{user.mention}"
    text, ent = add_random_emoji(text)

    await message.reply_text(text, entities=ent)


# ================= WATCH =================
@bot.on_message(filters.group)
async def afk_watcher(_, message: Message):
    if not message.from_user or message.from_user.is_bot:
        return

    targets = {}

    # ===== REPLY =====
    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        targets[u.id] = u

    # ===== MENTIONS =====
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

        text = sc(f"""
User is AFK

Last Seen : {duration}
Reason : {data.get('reason', 'Away')}
""")

        text = f"{text}\n\n{user.mention}"
        text, ent = add_random_emoji(text)

        await message.reply_text(text, entities=ent)
        
