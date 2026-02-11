import asyncio
import time
from pyrogram import filters
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.users import get_users, remove_user
from Bot.Database.stats import inc_lifetime
from Bot.Database.core import db


SUDO_USERS = [7952773964]


@bot.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")

    start_time = time.time()
    msg = message.reply_to_message

    total = 0
    success = 0
    failed = 0

    status = await message.reply(sc("broadcast started..."))

    async for user_id in get_users():
        total += 1

        try:
            await msg.copy(user_id)
            success += 1
            await asyncio.sleep(0.05)

        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await msg.copy(user_id)
                success += 1
            except Exception as er:
                print("Retry Fail:", user_id, er)
                failed += 1

        except (UserIsBlocked, PeerIdInvalid):
            failed += 1
            try:
                await remove_user(user_id)
            except:
                pass

        except Exception as e:
            print("Broadcast Error:", user_id, e)
            failed += 1

        # progress update every 100 users
        if total % 100 == 0:
            try:
                await status.edit(sc(f"broadcasting...\n\ndone : {total}"))
            except:
                pass

    # ===== save log =====
    await db.broadcasts.insert_one({
        "total": total,
        "success": success,
        "failed": failed,
        "time": int(time.time())
    })

    await inc_lifetime("broadcasts")

    taken = round(time.time() - start_time, 2)

    await status.edit(
        sc(f"""
broadcast completed

total users : {total}
success : {success}
failed : {failed}

time taken : {taken}s
""")
    )
    
