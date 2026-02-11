from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid
import asyncio

from Bot import bot
from config import SUDO_USERS

from Bot.Database.users import get_users, remove_user
from Bot.Database.stats import inc_lifetime
from Bot.Database.core import db


@bot.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        return await message.reply("Reply to message to broadcast.")

    msg = message.reply_to_message

    total = 0
    success = 0
    failed = 0

    status = await message.reply("📢 Broadcasting...")

    async for user_id in get_users():
        total += 1
        try:
            await msg.copy(user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await msg.copy(user_id)
            success += 1
        except (UserIsBlocked, PeerIdInvalid):
            failed += 1
            await remove_user(user_id)
        except:
            failed += 1

    # log
    await db.broadcasts.insert_one({
        "total": total,
        "success": success,
        "failed": failed,
    })
    await inc_lifetime("broadcasts")

    await status.edit(
        f"""
✅ **Broadcast Done**

👥 Total : {total}
✔ Success : {success}
❌ Failed : {failed}
"""
    )
  
