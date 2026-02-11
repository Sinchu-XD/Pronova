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
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )


# ================= BAN =================
@bot.on_message(filters.command("bban") & filters.group)
async def ban(_, m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    user = m.reply_to_message.from_user
    await ban_user(m.chat.id, user.id)

    await m.reply(sc(f"user banned from using bot\n\n{user.mention}"))


# ================= UNBAN =================
@bot.on_message(filters.command("bunban") & filters.group)
async def unban(_, m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    user = m.reply_to_message.from_user
    await unban_user(m.chat.id, user.id)

    await m.reply(sc(f"user unbanned\n\n{user.mention}"))


# ================= GBAN =================
@bot.on_message(filters.command("gban") & filters.user(SUDO_USERS))
async def gban(_, m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    user = m.reply_to_message.from_user
    await gban_user(user.id)

    await m.reply(sc(f"user globally banned\n\n{user.mention}"))


# ================= UNGBAN =================
@bot.on_message(filters.command("ungban") & filters.user(SUDO_USERS))
async def ungban(_, m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(sc("reply to user"))

    user = m.reply_to_message.from_user
    await ungban_user(user.id)

    await m.reply(sc(f"user globally unbanned\n\n{user.mention}"))


# ================= CHECK =================
@bot.on_message(filters.command("checkban"))
async def checkban(_, m):
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
@bot.on_message(filters.command("totalbanned") & filters.group)
async def total_banned_cmd(_, m):
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    users = await get_banned(m.chat.id)
    count = len(users)

    await m.reply(sc(f"total banned users : {count}"))


# ================= TOTAL GBANNED =================
@bot.on_message(filters.command("totalgbanned") & filters.user(SUDO_USERS))
async def total_gbanned_cmd(_, m):
    users = await get_gbanned()
    count = len(users)

    await m.reply(sc(f"total gbanned users : {count}"))
  
