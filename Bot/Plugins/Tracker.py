from pyrogram import filters

from Bot import bot
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat
from Bot.Database.Activity import update_gc_activity
from Bot.Database.Stats import inc_lifetime, inc_daily


# ================= MESSAGE TRACKER =================
@bot.on_message(filters.private | filters.group)
async def msg_tracker(_, message):
    try:
        if not message.from_user or message.from_user.is_bot:
            return

        await add_user(message.from_user)
        await add_chat(message.chat.id)

        if message.chat.type != "private":
            await update_gc_activity(
                message.chat.id,
                message.from_user.id
            )

        if message.command:
            await inc_lifetime("commands")
            await inc_daily("commands")

    except Exception as e:
        print("Tracker Error:", e)
      
