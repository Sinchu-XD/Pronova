import os
import asyncio
import importlib
import traceback
import signal

from AbhiCalls import idle, Plugin

from Bot import bot, user, engine

import Bot.Plugins.Music
import Bot.Plugins.Admins
import Bot.Plugins.CallBacks
import Bot.Plugins.Start
import Bot.Plugins.Afk
import Bot.Plugins.Broadcast
import Bot.Plugins.Stats
import Bot.Plugins.Bans
import Bot.Plugins.Info
import Bot.Plugins.Tracker
import Bot.Plugins.GetActivity
# ===== DATABASE =====
from Bot.Database.Core import setup_database

# ===== AUTO =====
from Bot.Plugins.GetActivity import daily_gc_report
from Bot.Helper.Assistant import setup_assistant


# ================= AUTO IMPORT =================
def auto_import(folder_path, module_path):
    print(f"\n📦 Loading {module_path}\n")

    loaded = 0
    failed = 0

    if not os.path.exists(folder_path):
        print("Folder not found.")
        return

    for file in os.listdir(folder_path):
        if not file.endswith(".py") or file.startswith("__"):
            continue

        name = file[:-3]

        try:
            importlib.import_module(f"{module_path}.{name}")
            print(f"✅ {name}")
            loaded += 1
        except Exception:
            print(f"❌ {name}")
            traceback.print_exc()
            failed += 1

    print(f"\nLoaded: {loaded} | Failed: {failed}")
    print("==============================\n")


# ================= LOAD EVERYTHING =================
def load_all_modules():
    auto_import("Bot/Database", "Bot.Database")
    auto_import("Bot/Helper", "Bot.Helper")
    auto_import("Bot/Plugins", "Bot.Plugins")


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

    print("📦 auto loading modules")
    load_all_modules()

    print("🤖 bot start")
    await bot.start()

    print("👤 assistant start")
    await user.start()

    print("🎙 engine start")
    await engine.start()

    print("🗄 database setup")
    await setup_database()

    print("⚙️ setup assistant")
    await setup_assistant()

    print("🔌 load vc plugin")
    engine.vc.load_plugin(Plugin(bot))

    # ===== HANDLER INFO =====
    print("\n📡 Handler Info")
    total = 0
    for group, handlers in bot.dispatcher.groups.items():
        print(f"Group {group}: {len(handlers)} handlers")
        total += len(handlers)
    print(f"Total Handlers: {total}\n")

    # ===== START AUTOMATION =====
    print("📊 starting daily report scheduler")
    asyncio.create_task(safe_task(daily_gc_report(bot), "DailyActivity"))

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
    
