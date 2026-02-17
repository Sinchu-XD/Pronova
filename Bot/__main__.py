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
import Bot.Helper.Font

# Database
import Bot.Database.Users
import Bot.Database.Chats
import Bot.Database.Stats
import Bot.Database.Bans
import Bot.Database.Afk
import Bot.Database.Ranking
import Bot.Database.Songs


# ===== IMPORT FUNCTIONS =====
from Bot.Database.Core import setup_database
from Bot.Helper.Assistant import setup_assistant

import random
from pyrogram import filters, enums
from pyrogram.types import MessageEntity

from Bot import bot, CUSTOM_EMOJI_IDS


# ===== Premium Left + Right Function =====
def premium_lr(text: str):
    left_id = random.choice(CUSTOM_EMOJI_IDS)
    right_id = random.choice(CUSTOM_EMOJI_IDS)

    new_text = f"❤️ {text} ❤️"

    entities = [
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=0,
            length=1,
            custom_emoji_id=left_id
        ),
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=len(new_text) - 1,
            length=1,
            custom_emoji_id=right_id
        )
    ]

    return new_text, entities


# ===== Test Command =====
@bot.on_message(filters.command("test"))
async def test_command(_, message):
    text, ent = premium_lr("Bot Working Fine 🔥")
    await message.reply(text, entities=ent)
    
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
    
