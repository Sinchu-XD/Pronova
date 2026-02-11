import os
import asyncio
import importlib
import traceback
import signal

from AbhiCalls import idle, Plugin
from pyrogram import filters

from Bot import bot, user, engine

# ===== DATABASE =====
from Bot.Database.Core import setup_database
from Bot.Database.Users import add_user
from Bot.Database.Chats import add_chat
from Bot.Database.Activity import update_gc_activity
from Bot.Database.Stats import inc_daily, inc_lifetime
import Bot.Plugins.Bans
import Bot.Plugins.Broadcast
import Bot.Plugins.Stats

# ===== AUTO =====
from Bot.Plugins.GetActivity import daily_gc_report

from Bot.Helper.Assistant import setup_assistant


# ================= PLUGIN LOADER =================
def load_plugins():
    print("\n📦 Loading Plugins...\n")

    PLUGINS = [
        "Music",
        "Admins",
        "CallBacks",
        "Start",
        "Afk",
        "GetActivity",
        "Broadcast",
        "Stats",
        "Bans"
    ]

    for plug in PLUGINS:
        try:
            importlib.import_module(f"Bot.Plugins.{plug}")
            print(f"✅ {plug}")
        except Exception:
            print(f"❌ {plug}")
            traceback.print_exc()

    print("==============================\n")


# ================= SAFE TASK =================
async def safe_task(coro, name):
    try:
        await coro
    except Exception:
        print(f"{name} crashed:")
        traceback.print_exc()


# ================= MAIN =================
async def main():
    os.environ["TEXT"] = "⚡ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

    # ✅ LOAD PLUGINS ONLY ONCE
    load_plugins()

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

    print("🔌 load vc plugin")
    engine.vc.load_plugin(Plugin(bot))

    # ========= GLOBAL TRACKER =========
    @bot.on_message(filters.private | filters.group)
    async def register(_, message):
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
            print("Register Error:", e)

    # ===== HANDLER INFO =====
    print("\n📡 Handler Info")
    total = 0
    for group, handlers in bot.dispatcher.groups.items():
        print(f"Group {group}: {len(handlers)} handlers")
        total += len(handlers)
    print(f"Total Handlers: {total}\n")

    # ===== START AUTOMATION =====
    print("📊 starting daily report scheduler")
    asyncio.create_task(safe_task(daily_gc_report(bot)))

    print("💤 bot running")
    await idle()


# ================= SHUTDOWN =================
async def shutdown():
    print("\n🛑 Shutting down...")
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
    
