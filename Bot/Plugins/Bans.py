from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot
from Bot.Helper.Font import sc

# ===== OWNER =====
SUDO_USERS = [7952773964]

# ===== DB =====
from Bot.Database.Bans import (
    ban_user, unban_user,
    gban_user, ungban_user,
    is_banned, is_gbanned,
    get_banned, get_gbanned
)


# ================= ADMIN CHECK =================
async def is_admin(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except Exception as e:
        print("Admin check error:", e)
        return False


# ================= SMALL DEBUG =================
def step(x):
    print(f"[BANS DEBUG] {x}")


# ================= BAN =================
@bot.on_message(filters.command("bban"))
async def ban(_, m):
    step("bban entered")

    if not m.from_user:
        step("no from user")
        return

    if not m.reply_to_message:
        step("no reply")
        return await m.reply(sc("reply to user"))

    if not m.reply_to_message.from_user:
        step("reply but invalid")
        return await m.reply(sc("invalid user"))

    if not await is_admin(m.chat.id, m.from_user.id):
        step("not admin")
        return await m.reply(sc("admins only"))

    user = m.reply_to_message.from_user

    await ban_user(m.chat.id, user.id)
    step("ban done")

    await m.reply(sc(f"user banned from using bot\n\n{user.mention}"))


# ================= UNBAN =================
@bot.on_message(filters.command("bunban"))
async def unban(_, m):
    step("bunban entered")

    if not m.from_user:
        return

    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    user = m.reply_to_message.from_user
    await unban_user(m.chat.id, user.id)

    step("unban done")
    await m.reply(sc(f"user unbanned\n\n{user.mention}"))


# ================= GBAN =================
@bot.on_message(filters.command("gban"))
async def gban(_, m):
    step("gban entered")

    if not m.from_user:
        step("no from user")
        return

    if m.from_user.id not in SUDO_USERS:
        step("not sudo")
        return await m.reply("sudo only")

    if not m.reply_to_message:
        step("no reply")
        return await m.reply(sc("reply to user"))

    if not m.reply_to_message.from_user:
        step("invalid reply")
        return await m.reply(sc("invalid user"))

    user = m.reply_to_message.from_user
    await gban_user(user.id)

    step("gban done")
    await m.reply(sc(f"user globally banned\n\n{user.mention}"))


# ================= UNGBAN =================
@bot.on_message(filters.command("ungban"))
async def ungban(_, m):
    step("ungban entered")

    if not m.from_user:
        return

    if m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    user = m.reply_to_message.from_user
    await ungban_user(user.id)

    step("ungban done")
    await m.reply(sc(f"user globally unbanned\n\n{user.mention}"))


# ================= CHECK =================
@bot.on_message(filters.command("checkban"))
async def checkban(_, m):
    step("checkban entered")

    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    user = m.reply_to_message.from_user
    uid = user.id

    if await is_gbanned(uid):
        return await m.reply(sc("user is gbanned"))

    if await is_banned(m.chat.id, uid):
        return await m.reply(sc("user is banned in this chat"))

    await m.reply(sc("user is free"))


# ================= TOTAL BANNED =================
@bot.on_message(filters.command("totalbanned"))
async def total_banned_cmd(_, m):
    step("totalbanned entered")

    if not m.from_user:
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    users = await get_banned(m.chat.id)
    count = len(users)

    await m.reply(sc(f"total banned users : {count}"))


# ================= TOTAL GBANNED =================
@bot.on_message(filters.command("totalgbanned"))
async def total_gbanned_cmd(_, m):
    step("totalgbanned entered")

    if not m.from_user:
        return

    if m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    users = await get_gbanned()
    count = len(users)

    await m.reply(sc(f"total gbanned users : {count}"))
    
