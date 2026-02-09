import os
from AbhiCalls import idle, Plugin

from Bot import bot, user, engine

import Bot.plugins.Music
import Bot.plugins.Admins
import Bot.plugins.Callbacks

from Bot.helpers.assistant import setup_assistant


async def main():
    os.environ["TEXT"] = "Powered By Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

    await bot.start()
    await user.start()
    await engine.start()

    await setup_assistant()

    engine.vc.load_plugin(Plugin(bot))
    await idle()


bot.run(main())
