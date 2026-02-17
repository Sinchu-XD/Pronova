print("STATS PLUGIN LOADED")

from pyrogram import filters

from Bot import bot
from Bot.Helper.Font import sc
from Bot.Helper.Emoji import add_premium_lr

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


@bot.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats(_, m):

    loading_text, ent = add_premium_lr(sc("fetching analytics"))
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
        fail_text, ent = add_premium_lr(sc("failed to fetch stats"))
        return await msg.edit(fail_text, entities=ent)

    text = f"{sc('bot analytics')}\n\n"

    text += f"{sc('users')} : {users}\n"
    text += f"{sc('chats')} : {chats}\n"
    text += f"{sc('songs')} : {songs}\n"
    text += f"{sc('commands')} : {commands}\n\n"

    text += f"{sc('banned groups')} : {banned}\n"
    text += f"{sc('gbanned global')} : {gbanned}\n\n"

    text += f"{sc('growth')}\n"
    text += f"7 {sc('days')} : {weekly_users}\n"
    text += f"30 {sc('days')} : {monthly_users}\n\n"

    text += f"{sc('top groups')}\n"

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

    text += f"\n{sc('top users')}\n"

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

    text += f"\n{sc('most played')}\n"

    if mp:
        for i, (name, c) in enumerate(mp, 1):
            text += f"{i}. {name} → {c}\n"
    else:
        text += f"{sc('no data')}\n"

    final_text, ent = add_premium_lr(text)

    try:
        await msg.edit(final_text, entities=ent)
    except Exception as e:
        print("Stats Edit Error:", e)
        
