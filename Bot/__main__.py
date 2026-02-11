import os
import asyncio

from AbhiCalls import idle, Plugin
from pyrogram import filters

from Bot import bot, user, engine

# ===== DATABASE =====
from Bot.Database.Core import setup_database
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat
from Bot.Database.Activity import update_gc_activity
from Bot.Database.Stats import inc_daily, inc_lifetime

# ===== AUTO =====
from Bot.Plugins.GetActivity import daily_gc_report

# ===== PLUGINS =====
import Bot.Plugins.Music
import Bot.Plugins.Admins
import Bot.Plugins.CallBacks
import Bot.Plugins.Start
import Bot.Plugins.Afk
import Bot.Plugins.GetActivity
import Bot.Plugins.Broadcast
import Bot.Plugins.Stats

from Bot.Helper.Assistant import setup_assistant


async def main():
    os.environ["TEXT"] = "⚡ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

    print("🤖 bot start")
    await bot.start()

    print("👤 assistant start")
    await user.start()

    print("🎙 engine start")
    await engine.start()

    print("⚙️ setup assistant")
    await setup_assistant()

    print("🗄 database setup")
    await setup_database()

    print("🔌 load plugin")
    engine.vc.load_plugin(Plugin(bot))

    # ===== START AUTOMATION =====
    print("📊 starting daily report scheduler")
    asyncio.create_task(daily_gc_report(bot))

    # ========= GLOBAL TRACKER =========
    @bot.on_message(filters.private | filters.group)
    async def register(_, message):
        try:
            if not message.from_user:
                return

            if message.from_user.is_bot:
                return

            await add_user(message.from_user)
            await add_chat(message.chat.id)

            if message.chat.type != "private":
                await update_gc_activity(
                    message.chat.id,
                    message.from_user.id
                )

            # auto command analytics
            if message.command:
                await inc_lifetime("commands")
                await inc_daily("commands")

        except Exception as e:
            print("Register Error:", e)

    print("💤 bot running")
    await idle()


if __name__ == "__main__":
    bot.loop.run_until_complete(main())
    
