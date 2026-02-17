
print("BANS PLUGIN LOADED")

import random
from pyrogram import filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import MessageEntity

from Bot import bot, CUSTOM_EMOJI_IDS
from Bot.Helper.Font import sc
from Bot.Database.Bans import (
    ban_user, unban_user,
    gban_user, ungban_user,
    is_banned, is_gbanned,
    get_banned, get_gbanned
)

SUDO_USERS = [7952773964]


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
        text, ent = add_random_emoji(sc("admins only"))
        return await m.reply(text, entities=ent)

    target = get_target(m)
    if not target:
        text, ent = add_random_emoji(sc("reply to user"))
        return await m.reply(text, entities=ent)

    if protected(target):
        text, ent = add_random_emoji(sc("cannot ban this user"))
        return await m.reply(text, entities=ent)

    await ban_user(m.chat.id, target.id)

    text = f"{sc('user banned from using bot')}\n\n{target.mention}"
    text, ent = add_random_emoji(text)
    await m.reply(text, entities=ent)


# ================= UNBAN =================
@bot.on_message(filters.command("bunban"))
async def unban(_, m):
    if not m.from_user:
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        text, ent = add_random_emoji(sc("admins only"))
        return await m.reply(text, entities=ent)

    target = get_target(m)
    if not target:
        text, ent = add_random_emoji(sc("reply to user"))
        return await m.reply(text, entities=ent)

    await unban_user(m.chat.id, target.id)

    text = f"{sc('user unbanned')}\n\n{target.mention}"
    text, ent = add_random_emoji(text)
    await m.reply(text, entities=ent)


# ================= GBAN =================
@bot.on_message(filters.command("gban"))
async def gban(_, m):
    if not m.from_user or m.from_user.id not in SUDO_USERS:
        text, ent = add_random_emoji("sudo only")
        return await m.reply(text, entities=ent)

    target = get_target(m)
    if not target:
        text, ent = add_random_emoji(sc("reply to user"))
        return await m.reply(text, entities=ent)

    if protected(target):
        text, ent = add_random_emoji(sc("cannot gban this user"))
        return await m.reply(text, entities=ent)

    await gban_user(target.id)

    text = f"{sc('user globally banned')}\n\n{target.mention}"
    text, ent = add_random_emoji(text)
    await m.reply(text, entities=ent)


# ================= UNGBAN =================
@bot.on_message(filters.command("ungban"))
async def ungban(_, m):
    if not m.from_user or m.from_user.id not in SUDO_USERS:
        text, ent = add_random_emoji("sudo only")
        return await m.reply(text, entities=ent)

    target = get_target(m)
    if not target:
        text, ent = add_random_emoji(sc("reply to user"))
        return await m.reply(text, entities=ent)

    await ungban_user(target.id)

    text = f"{sc('user globally unbanned')}\n\n{target.mention}"
    text, ent = add_random_emoji(text)
    await m.reply(text, entities=ent)


# ================= CHECK =================
@bot.on_message(filters.command("checkban"))
async def checkban(_, m):
    target = get_target(m)
    if not target:
        text, ent = add_random_emoji(sc("reply to user"))
        return await m.reply(text, entities=ent)

    if await is_gbanned(target.id):
        text, ent = add_random_emoji(sc("user is gbanned"))
        return await m.reply(text, entities=ent)

    if await is_banned(m.chat.id, target.id):
        text, ent = add_random_emoji(sc("user is banned in this chat"))
        return await m.reply(text, entities=ent)

    text, ent = add_random_emoji(sc("user is free"))
    await m.reply(text, entities=ent)


# ================= TOTAL BANNED =================
@bot.on_message(filters.command("totalbanned"))
async def total_banned_cmd(_, m):
    if not m.from_user:
        return

    if not await is_admin(m.chat.id, m.from_user.id):
        text, ent = add_random_emoji(sc("admins only"))
        return await m.reply(text, entities=ent)

    users = await get_banned(m.chat.id)
    text, ent = add_random_emoji(f"{sc('total banned users')} : {len(users)}")
    await m.reply(text, entities=ent)


# ================= TOTAL GBANNED =================
@bot.on_message(filters.command("totalgbanned"))
async def total_gbanned_cmd(_, m):
    if not m.from_user or m.from_user.id not in SUDO_USERS:
        text, ent = add_random_emoji("sudo only")
        return await m.reply(text, entities=ent)

    users = await get_gbanned()
    text, ent = add_random_emoji(f"{sc('total gbanned users')} : {len(users)}")
    await m.reply(text, entities=ent)
    
