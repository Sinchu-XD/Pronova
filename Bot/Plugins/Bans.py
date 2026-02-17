print("BANS PLUGIN LOADED")
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
    except:
        return False


# ================= HELPERS =================
def get_target(m):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return None
    return m.reply_to_message.from_user


def protected(target):
    if not target:
        return True
    if target.is_bot:
        return True
    if target.id in SUDO_USERS:
        return True
    return False


# ================= BAN =================
@bot.on_message(filters.command("bban"))
async def ban(_, m):
    if not m.from_user:
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    if protected(target):
        return await m.reply(sc("cannot ban this user"))

    await ban_user(m.chat.id, target.id)

    text = sc("user banned from using bot")
    await m.reply(f"{text}\n\n{target.mention}")


# ================= UNBAN =================
@bot.on_message(filters.command("bunban"))
async def unban(_, m):
    if not m.from_user:
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply(sc("admins only"))

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    await unban_user(m.chat.id, target.id)

    text = sc("user unbanned")
    await m.reply(f"{text}\n\n{target.mention}")


# ================= GBAN =================
@bot.on_message(filters.command("gban"))
async def gban(_, m):
    if not m.from_user or m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    if protected(target):
        return await m.reply(sc("cannot gban this user"))

    await gban_user(target.id)

    text = sc("user globally banned")
    await m.reply(f"{text}\n\n{target.mention}")


# ================= UNGBAN =================
@bot.on_message(filters.command("ungban"))
async def ungban(_, m):
    if not m.from_user or m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    await ungban_user(target.id)

    text = sc("user globally unbanned")
    await m.reply(f"{text}\n\n{target.mention}")


# ================= CHECK =================
@bot.on_message(filters.command("checkban"))
async def checkban(_, m):
    target = get_target(m)
    if not target:
        return await m.reply(sc("reply to user"))

    if await is_gbanned(target.id):
        return await m.reply(sc("user is gbanned"))

    if await is_banned(m.chat.id, target.id):
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
    await m.reply(f"{sc('total banned users')} : {len(users)}")


# ================= TOTAL GBANNED =================
@bot.on_message(filters.command("totalgbanned"))
async def total_gbanned_cmd(_, m):
    if not m.from_user or m.from_user.id not in SUDO_USERS:
        return await m.reply("sudo only")

    users = await get_gbanned()
    await m.reply(f"{sc('total gbanned users')} : {len(users)}")
