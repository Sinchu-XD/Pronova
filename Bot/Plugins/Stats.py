from pyrogram import filters

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.Users import total_users
from Bot.Database.Chats import total_chats
from Bot.Database.Songs import most_played
from Bot.Database.Ranking import top_groups, top_users
from Bot.Database.Stats import get_lifetime, sum_range
from Bot.Database.Bans import total_banned, get_gbanned


# ===== OWNER =====
SUDO_USERS = [7952773964]


@bot.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats(_, m):
    msg = await m.reply(sc("fetching analytics..."))

    try:
        users = await total_users()
        chats = await total_chats()
        songs = await get_lifetime("songs")
        commands = await get_lifetime("commands")

        banned = await total_banned()

        # safer (avoid heavy in future)
        gbanned = len(await get_gbanned())

        weekly_users = await sum_range(7, "users")
        monthly_users = await sum_range(30, "users")

        tg = await top_groups(3)
        tu = await top_users(3)
        mp = await most_played(3)

    except Exception as e:
        print("Stats Fetch Error:", e)
        return await msg.edit(sc("failed to fetch stats"))

    text = f"""
BOT ANALYTICS

Users : {users}
Chats : {chats}
Songs : {songs}
Commands : {commands}

Banned (groups) : {banned}
Gbanned (global) : {gbanned}

Growth
7 Days : {weekly_users}
30 Days : {monthly_users}

Top Groups
"""

    if tg:
        for i, (cid, s) in enumerate(tg, 1):
            text += f"{i}. {cid} → {s}\n"
    else:
        text += "No data\n"

    text += "\nTop Users\n"

    if tu:
        for i, (uid, c) in enumerate(tu, 1):
            text += f"{i}. {uid} → {c}\n"
    else:
        text += "No data\n"

    text += "\nMost Played\n"

    if mp:
        for i, (name, c) in enumerate(mp, 1):
            text += f"{i}. {name} → {c}\n"
    else:
        text += "No data\n"

    try:
        await msg.edit(sc(text))
    except Exception as e:
        print("Stats Edit Error:", e)
        
