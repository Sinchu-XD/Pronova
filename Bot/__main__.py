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


# ================= GLOBAL TRACKER =================
@bot.on_message(filters.private | filters.group)
async def register(_, message):
    try:
        if not message.from_user or message.from_user.is_bot:
            return

        await add_user(message.from_user)
        await add_chat(message.chat)

        if message.chat.type != "private":
            await update_gc_activity(message.chat, message.from_user)

        if message.command:
            await inc_lifetime("commands")
            await inc_daily("commands")

    except Exception as e:
        print("Register Error:", e)


# ================= MAIN =================
async def main():
    os.environ["TEXT"] = "⚡ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

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

    print("📦 auto loading modules")
    load_all_modules()

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
    
