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
  
