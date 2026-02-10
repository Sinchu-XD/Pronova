import time
from pyrogram import filters
from pyrogram.types import Message
from Bot import bot


# ================= STORAGE =================
# user_id : {reason, time}
AFK_USERS = {}

# cooldown for mention spam
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

    AFK_USERS[user.id] = {
        "reason": reason,
        "time": time.time()
    }

    await message.reply_text(
        f"""
🌙 **AFK Enabled**

👤 {user.mention}
📝 𝗥𝗲𝗮𝘀𝗼𝗻 : `{reason}`

I will inform anyone who mentions you.
"""
    )


# ================= AUTO REMOVE AFK =================
# ANY MESSAGE from that user = back
@bot.on_message(filters.all & ~filters.command("afk"))
async def auto_remove_afk(_, message: Message):
    user = message.from_user
    if not user:
        return

    if user.id in AFK_USERS:
        data = AFK_USERS[user.id]
        duration = format_time(time.time() - data["time"])

        del AFK_USERS[user.id]

        await message.reply_text(
            f"""
✨ **Welcome Back**

👤 {user.mention}
🕒 Away for `{duration}`
"""
        )


# ================= WATCH TAG / REPLY =================
@bot.on_message(filters.group)
async def afk_watcher(_, message: Message):
    if not message.from_user:
        return

    targets = []

    # reply target
    if message.reply_to_message and message.reply_to_message.from_user:
        targets.append(message.reply_to_message.from_user)

    # mention target
    if message.mentions:
        targets.extend(message.mentions)

    for user in targets:
        if user.id not in AFK_USERS:
            continue

        # anti spam → 15 sec per user per chat
        key = (message.chat.id, user.id)
        last = LAST_REPLY.get(key, 0)

        if time.time() - last < 15:
            continue

        LAST_REPLY[key] = time.time()

        data = AFK_USERS[user.id]
        duration = format_time(time.time() - data["time"])

        await message.reply_text(
            f"""
🌙 **User is AFK**

👤 {user.mention}
🕒 𝗟𝗮𝘀𝘁 𝗦𝗲𝗲𝗻 : `{duration}`
📝 𝗥𝗲𝗮𝘀𝗼𝗻 : `{data['reason']}`
"""
        )
        
