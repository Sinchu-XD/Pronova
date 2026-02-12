from pyrogram import filters

from Bot import bot
from Bot.Database.Activity import get_gc_activity
from Bot.Helper.Font import sc


USER_CACHE = {}


@bot.on_message(filters.command("info") & filters.group)
async def group_info(_, message):
    chat_id = message.chat.id

    data = await get_gc_activity(chat_id)

    if not data:
        return await message.reply(sc("no activity data"))

    users = data.get("users", {})
    total_messages = int(data.get("total_messages", 0))

    if not users and not total_messages:
        return await message.reply(sc("no activity yet"))

    active_users = len(users)

    # ===== HEADER =====
    text = f"📊 {sc('live activity report')}\n\n"
    text += f"🏠 {sc('group')} : {message.chat.title}\n\n"
    text += f"👥 {sc('active users')} : {active_users}\n"
    text += f"💬 {sc('total messages')} : {total_messages}\n\n"

    text += f"🏆 {sc('top users')}\n"

    # ===== TOP USERS =====
    top = sorted(
        users.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (uid, count) in enumerate(top, start=1):
        try:
            uid = int(uid)

            if uid in USER_CACHE:
                mention = USER_CACHE[uid]
            else:
                user = await bot.get_users(uid)
                mention = user.mention
                USER_CACHE[uid] = mention

        except:
            mention = f"`{uid}`"

        text += f"{i}. {mention} → {count}\n"

    await message.reply(text)
  
