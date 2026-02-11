import time
from pyrogram import filters
from pyrogram.types import Message

from Bot import bot
from Bot.Helper.Font import sc
from Bot.Database.Afk import set_afk_db, get_afk, remove_afk_db


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
    user = message.from_user
    if not user:
        return

    reason = "Away"
    if len(message.command) > 1:
        reason = " ".join(message.command[1:])

    await set_afk_db(user.id, reason)

    text = sc(f"""
AFK Enabled

Reason : {reason}

I will inform anyone who mentions you.
""")

    await message.reply_text(f"{text}\n\n{user.mention}")


# ================= AUTO REMOVE =================
@bot.on_message(filters.all & ~filters.command("afk"))
async def auto_remove_afk(_, message: Message):
    user = message.from_user
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

    text = sc(f"""
Welcome Back

Away for : {duration}
""")

    await message.reply_text(f"{text}\n\n{user.mention}")


# ================= WATCH =================
@bot.on_message(filters.group)
async def afk_watcher(_, message: Message):
    if not message.from_user:
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
        except Exception:
            since = time.time()

        duration = format_time(time.time() - since)

        text = sc(f"""
User is AFK

Last Seen : {duration}
Reason : {data.get('reason', 'Away')}
""")

        await message.reply_text(f"{text}\n\n{user.mention}")

import asyncio
import time
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid

from Bot import bot
from Bot.Helper.Font import sc

# ===== DATABASE =====
from Bot.Database.Users import get_users, remove_user, total_users
from Bot.Database.Chats import total_chats
from Bot.Database.Songs import most_played
from Bot.Database.Ranking import top_groups, top_users
from Bot.Database.Stats import get_lifetime, sum_range, inc_lifetime
from Bot.Database.Bans import (
    ban_user, unban_user,
    gban_user, ungban_user,
    is_banned, is_gbanned,
    get_banned, get_gbanned, total_banned
)
from Bot.Database.Core import db


# ========= CHANGE THIS =========
SUDO_USERS = [7952773964]
# =================================


# ================= ADMIN =================
async def is_admin(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except:
        return False


# ================= HELPER =================
def get_target(m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return None
    return m.reply_to_message.from_user


# =========================================================
# ======================= STATS ===========================
# =========================================================
@bot.on_message(filters.command("stats"))
async def stats(_, m):
    print("STATS HIT FROM:", m.from_user.id)

    if m.from_user.id not in SUDO_USERS:
        print("NOT SUDO")
        return await m.reply("NOT SUDO")

    print("SUDO OK")

    msg = await m.reply(sc("fetching analytics..."))

    users = await total_users()
    chats = await total_chats()
    songs = await get_lifetime("songs")
    commands = await get_lifetime("commands")
    banned = await total_banned()
    gbanned = await db.gbanned.count_documents({})

    weekly_users = await sum_range(7, "users")
    monthly_users = await sum_range(30, "users")

    tg = await top_groups(3)
    tu = await top_users(3)
    mp = await most_played(3)

    text = f"""
BOT ANALYTICS

Users : {users}
Chats : {chats}
Songs : {songs}
Commands : {commands}

Banned : {banned}
Gbanned : {gbanned}

Growth
7 Days : {weekly_users}
30 Days : {monthly_users}
"""

    await msg.edit(sc(text))


# =========================================================
# ======================= BROADCAST =======================
# =========================================================
@bot.on_message(filters.command("broadcast"))
async def broadcast(_, message):
    print("BROADCAST HIT FROM:", message.from_user.id)

    if message.from_user.id not in SUDO_USERS:
        print("NOT SUDO")
        return await message.reply("NOT SUDO")

    if not message.reply_to_message:
        return await message.reply("Reply to a message.")

    start = time.time()
    msg = message.reply_to_message

    total = success = failed = 0

    status = await message.reply(sc("broadcast started..."))

    async for user_id in get_users():
        total += 1
        try:
            await msg.copy(user_id)
            success += 1
            await asyncio.sleep(0.2)

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except (UserIsBlocked, PeerIdInvalid):
            failed += 1
            await remove_user(user_id)
        except:
            failed += 1

    await inc_lifetime("broadcasts")

    taken = round(time.time() - start, 2)

    await status.edit(sc(f"done\nsuccess {success}\nfailed {failed}\ntime {taken}s"))


# =========================================================
# ======================= BBAN ============================
# =========================================================
@bot.on_message(filters.command("bban"))
async def bban(_, m):
    print("BBAN HIT FROM:", m.from_user.id)

    if m.from_user.id not in SUDO_USERS and not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply("NOT ALLOWED")

    target = get_target(m)
    if not target:
        return await m.reply("reply to user")

    await ban_user(m.chat.id, target.id)

    text = sc("user banned")
    await m.reply(f"{text}\n\n{target.mention}")
    
