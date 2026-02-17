from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Assistant import get_ass
from Bot.Helper.Emoji import add_premium

from Bot.Database.Songs import inc_song_play
from Bot.Database.Bans import is_banned, is_gbanned
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat


async def is_admin(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except:
        return False


async def check_ban(m):
    if not m.from_user:
        return True

    uid = m.from_user.id
    chat_id = m.chat.id

    if await is_gbanned(uid):
        text, ent = add_premium("You are gbanned")
        await m.reply(text, entities=ent)
        return True

    if await is_banned(chat_id, uid):
        text, ent = add_premium("You are banned in this chat")
        await m.reply(text, entities=ent)
        return True

    return False


async def handle_play(m, force=False):

    if await check_ban(m):
        return

    if not m.from_user:
        return

    chat_id = m.chat.id
    uid = m.from_user.id

    if force and not await is_admin(chat_id, uid):
        text, ent = add_premium("Admins only")
        return await m.reply(text, entities=ent)

    if not await get_ass(chat_id, m):
        return

    query = m.text.split(None, 1)[1] if len(m.command) > 1 else None

    if not query:
        text, ent = add_premium("Give song name")
        return await m.reply(text, entities=ent)

    try:
        song, title = await engine.vc.play(
            chat_id,
            query,
            m.from_user.mention
        )
    except:
        text, ent = add_premium("Unable to play song")
        return await m.reply(text, entities=ent)

    if not song:
        text, ent = add_premium("Unable to play song")
        return await m.reply(text, entities=ent)

    await inc_song_play(chat_id, title or query)

    text, ent = add_premium(f"Now Playing: {title or query}")
    await m.reply(text, entities=ent)


@bot.on_message(filters.command("play"))
async def play(_, m):
    await handle_play(m, force=False)


@bot.on_message(filters.command("debug"))
async def debug(_, message):
    text, ent = add_premium("Hello World")
    await message.reply(text, entities=ent)
    
