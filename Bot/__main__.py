import os
import asyncio
import signal

from AbhiCalls import idle, Plugin

from Bot import bot, user, engine


# ================= MANUAL IMPORT =================

# Plugins
import Bot.Plugins.Music
import Bot.Plugins.Admins
import Bot.Plugins.CallBacks
import Bot.Plugins.Start
import Bot.Plugins.Afk
import Bot.Plugins.Broadcast
import Bot.Plugins.Stats
import Bot.Plugins.Bans

# Helpers
import Bot.Helper.Assistant
import Bot.Helper.Font

# Database
import Bot.Database.Core
import Bot.Database.Users
import Bot.Database.Chats
import Bot.Database.Activity
import Bot.Database.Stats
import Bot.Database.Bans
import Bot.Database.Afk
import Bot.Database.Ranking
import Bot.Database.Songs


# ===== IMPORT FUNCTIONS =====
from Bot.Database.Core import setup_database
from Bot.Helper.Assistant import setup_assistant

# ================= SAFE TASK =================
async def safe_task(coro, name):
    try:
        await coro
    except Exception:
        print(f"{name} crashed")


# ================= MAIN =================
async def main():
    os.environ["TEXT"] = "⚡ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

    print("🤖 Starting Bot")
    await bot.start()

    print("👤 Starting Assistant")
    await user.start()

    print("🎙 Starting Engine")
    await engine.start()

    print("🗄 Connecting Database")
    await setup_database()

    print("⚙️ Loading Assistant Data")
    await setup_assistant()

    print("🔌 VC Plugin Attach")
    engine.vc.load_plugin(Plugin(bot))

    # ===== HANDLER INFO =====
    total = 0
    for _, handlers in bot.dispatcher.groups.items():
        total += len(handlers)
    print(f"📡 Handlers Loaded: {total}")


    print("✅ Bot is running")
    await idle()


# ================= SHUTDOWN =================
async def shutdown():
    print("🛑 Shutting down...")
    try:
        await engine.stop()
    except:
        pass
    try:
        await user.stop()
    except:
        pass
    try:
        await bot.stop()
    except:
        pass


if __name__ == "__main__":
    loop = bot.loop

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    loop.run_until_complete(main())
    
