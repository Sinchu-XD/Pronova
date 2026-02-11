import asyncio
import time
from pyrogram import filters
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid

from Bot import bot
from Bot.Helper.Font import sc

from Bot.Database.Users import get_users, remove_user
from Bot.Database.Stats import inc_lifetime
from Bot.Database.Core import db


SUDO_USERS = [7952773964]


# speed control (safe)
DELAY = 0.25


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
            await asyncio.sleep(DELAY)

        except FloodWait as e:
            print(f"FloodWait {e.value}s")
            await asyncio.sleep(e.value + 1)

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

        # progress every 200
        if total % 200 == 0:
            try:
                await status.edit(
                    sc(f"broadcasting...\n\nprocessed : {total}")
                )
            except:
                pass

    # ===== LOG =====
    try:
        await db.broadcasts.insert_one({
            "total": total,
            "success": success,
            "failed": failed,
            "time": int(time.time())
        })
    except Exception as e:
        print("Log Error:", e)

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
    
