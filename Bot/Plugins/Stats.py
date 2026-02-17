print("STATS PLUGIN LOADED")

import random
from pyrogram import filters, enums
from pyrogram.types import MessageEntity

from Bot import bot, CUSTOM_EMOJI_IDS
from Bot.Helper.Font import sc

from Bot.Database.Users import total_users
from Bot.Database.Chats import total_chats
from Bot.Database.Songs import most_played
from Bot.Database.Ranking import top_groups, top_users
from Bot.Database.Stats import get_lifetime, sum_range
from Bot.Database.Bans import total_banned
from Bot.Database.Core import db


SUDO_USERS = [7952773964]

USER_CACHE = {}
CHAT_CACHE = {}


# ================= PREMIUM LEFT + RIGHT =================
def inject_premium_lr(text: str):
    lines = text.split("\n")
    final_text = ""
    entities = []
    offset = 0

    for line in lines:
        left_id = random.choice(CUSTOM_EMOJI_IDS)
        right_id = random.choice(CUSTOM_EMOJI_IDS)

        new_line = f"❤️ {line} ❤️"
        final_text += new_line + "\n"

        # Left emoji entity
        entities.append(
            MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset,
                length=1,
                custom_emoji_id=left_id
            )
        )

        # Right emoji entity
        entities.append(
            MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset + len(new_line) - 1,
                length=1,
                custom_emoji_id=right_id
            )
        )

        offset += len(new_line) + 1

    final_text = final_text.rstrip("\n")
    return final_text, entities


@bot.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats(_, m):

    loading_text, ent = inject_premium_lr(sc("fetching analytics..."))
    msg = await m.reply(loading_text, entities=ent)

    try:
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

    except Exception as e:
        print("Stats Fetch Error:", e)
        fail_text, ent = inject_premium_lr(sc("failed to fetch stats"))
        return await msg.edit(fail_text, entities=ent)

    text = f"📊 {sc('bot analytics')}\n\n"

    text += f"{sc('users')} : {users}\n"
    text += f"{sc('chats')} : {chats}\n"
    text += f"{sc('songs')} : {songs}\n"
    text += f"{sc('commands')} : {commands}\n\n"

    text += f"{sc('banned (groups)')} : {banned}\n"
    text += f"{sc('gbanned (global)')} : {gbanned}\n\n"

    text += f"📈 {sc('growth')}\n"
    text += f"7 {sc('days')} : {weekly_users}\n"
    text += f"30 {sc('days')} : {monthly_users}\n\n"

    text += f"🏆 {sc('top groups')}\n"

    if tg:
        for i, (cid, s) in enumerate(tg, 1):
            try:
                cid = int(cid)
                if cid in CHAT_CACHE:
                    name = CHAT_CACHE[cid]
                else:
                    chat = await bot.get_chat(cid)
                    name = chat.title
                    CHAT_CACHE[cid] = name
            except:
                name = cid

            text += f"{i}. {name} → {s}\n"
    else:
        text += f"{sc('no data')}\n"

    text += f"\n👤 {sc('top users')}\n"

    if tu:
        for i, (uid, c) in enumerate(tu, 1):
            try:
                uid = int(uid)
                if uid in USER_CACHE:
                    mention = USER_CACHE[uid]
                else:
                    user = await bot.get_users(uid)
                    mention = user.mention
                    USER_CACHE[uid] = mention
            except:
                mention = uid

            text += f"{i}. {mention} → {c}\n"
    else:
        text += f"{sc('no data')}\n"

    text += f"\n🎧 {sc('most played')}\n"

    if mp:
        for i, (name, c) in enumerate(mp, 1):
            text += f"{i}. {name} → {c}\n"
    else:
        text += f"{sc('no data')}\n"

    final_text, ent = inject_premium_lr(text)

    try:
        await msg.edit(final_text, entities=ent)
    except Exception as e:
        print("Stats Edit Error:", e)
        
