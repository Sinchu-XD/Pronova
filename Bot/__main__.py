import os
import asyncio
from AbhiCalls import idle, Plugin

from Bot import bot, user, engine

import Bot.Plugins.Music
import Bot.Plugins.Admins
import Bot.Plugins.CallBacks

from Bot.Helper.Assistant import setup_assistant


async def main():
    os.environ["TEXT"] = "Powered By Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

    print("🤖 bot start")
    await bot.start()

    print("👤 assistant start")
    await user.start()

    print("🎙 engine start")
    await engine.start()

    print("⚙️ setup assistant")
    await setup_assistant()

    print("🔌 load plugin")
    engine.vc.load_plugin(Plugin(bot))

    print("💤 idle")
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
