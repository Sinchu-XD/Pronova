from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.Bans import (
    ban_user, unban_user,
    gban_user, ungban_user,
    is_banned, is_gbanned,
    get_banned, get_gbanned
)


# ================= OWNER =================
SUDO_USERS = [7952773964]


# ================= ADMIN =================
async def is_admin(chat_id, user_id):
    if not user_id:
        return False

    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except Exception as e:
        print("Admin check error:", e)
        return False


# ================= HELPERS =================
def get_target(m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return None
    return m.reply_to_message.from_user


# ================= BAN =================
@bot.on_message(filters.command("bban"))
async def ban(_, m):
    if not m.from_user:
        return

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    await ban_user(m.chat.id, target.id)
    await m.reply(sc(f"user banned from using bot\n\n{target.mention}"))


# ================= UNBAN =================
@bot.on_message(filters.command("bunban"))
async def unban(_, m):
    if not m.from_user:
        return

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    await unban_user(m.chat.id, target.id)
    await m.reply(sc(f"user unbanned\n\n{target.mention}"))


# ================= GBAN =================
@bot.on_message(filters.command("gban"))
async def gban(_, m):
    if not m.from_user:
        return

    if m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    await gban_user(target.id)
    await m.reply(sc(f"user globally banned\n\n{target.mention}"))


# ================= UNGBAN =================
@bot.on_message(filters.command("ungban"))
async def ungban(_, m):
    if not m.from_user:
        return

    if m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    await ungban_user(target.id)
    await m.reply(sc(f"user globally unbanned\n\n{target.mention}"))


# ================= CHECK =================
@bot.on_message(filters.command("checkban"))
async def checkban(_, m):
    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    uid = target.id

    if await is_gbanned(uid):
        return await m.reply(sc("user is gbanned"))

    if await is_banned(m.chat.id, uid):
        return await m.reply(sc("user is banned in this chat"))

    await m.reply(sc("user is free"))


# ================= TOTAL BANNED =================
@bot.on_message(filters.command("totalbanned"))
async def total_banned_cmd(_, m):
    if not m.from_user:
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    users = await get_banned(m.chat.id)
    await m.reply(sc(f"total banned users : {len(users)}"))


# ================= TOTAL GBANNED =================
@bot.on_message(filters.command("totalgbanned"))
async def total_gbanned_cmd(_, m):
    if not m.from_user:
        return

    if m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    users = await get_gbanned()
    await m.reply(sc(f"total gbanned users : {len(users)}"))
    
