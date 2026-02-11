from pyrogram import filters

from Bot import bot
from config import SUDO_USERS

from Bot.Database.Users import total_users
from Bot.Database.Chats import total_chats
from Bot.Database.Songs import most_played
from Bot.Database.Ranking import top_groups, top_users
from Bot.Database.Stats import get_lifetime, sum_range
from Bot.Database.Bans import total_banned


@bot.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats(_, m):
    users = await total_users()
    chats = await total_chats()
    songs = await get_lifetime("songs")
    commands = await get_lifetime("commands")
    banned = await total_banned()

    weekly_users = await sum_range(7, "users")
    monthly_users = await sum_range(30, "users")

    tg = await top_groups(3)
    tu = await top_users(3)
    mp = await most_played(3)

    text = f"""
📊 **BOT ANALYTICS**

👥 Users : {users}
💬 Chats : {chats}
🎵 Songs : {songs}
🛠 Commands : {commands}
🚫 Banned : {banned}

📈 **Growth**
7 Days : {weekly_users}
30 Days : {monthly_users}

🏆 **Top Groups**
"""

    for i, (cid, s) in enumerate(tg, 1):
        text += f"{i}. `{cid}` → {s}\n"

    text += "\n🏆 **Top Users**\n"
    for i, (uid, c) in enumerate(tu, 1):
        text += f"{i}. `{uid}` → {c}\n"

    text += "\n🔥 **Most Played**\n"
    for i, (name, c) in enumerate(mp, 1):
        text += f"{i}. {name} → {c}\n"

    await m.reply(text)
  
