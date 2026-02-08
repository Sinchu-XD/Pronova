import os
from AbhiCalls import idle, Plugin

from Bot import bot, user, engine, ASSISTANT_ID, ASSISTANT_USERNAME, Music  # handlers import

async def main():
    os.environ["TEXT"] = "Powered By Abhishek ✨"
    os.environ["LINK"] = "https://t.me/Her4Eva"

    await bot.start()
    await user.start()
    await engine.start()

    # fetch assistant
    me = await user.get_me()
    Music.ASSISTANT_ID = me.id
    Music.ASSISTANT_USERNAME = me.username or "NoUsername"

    engine.vc.load_plugin(Plugin(bot))
    await idle()

bot.run(main())
