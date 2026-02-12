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

DELAY = 0.25
PROGRESS_EVERY = 200


@bot.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")

    start_time = time.time()
    msg = message.reply_to_message

    total = 0
    success = 0
    failed = 0

    # ⭐ ANTI DUPLICATE
    sent_users = set()

    status = await message.reply(sc("broadcast started..."))

    async for user_id in get_users():
        uid = int(user_id)

        # ===== STOP DUPLICATE =====
        if uid in sent_users:
            continue

        sent_users.add(uid)
        total += 1

        try:
            await msg.copy(uid)
            success += 1
            await asyncio.sleep(DELAY)

        except FloodWait as e:
            print(f"FloodWait {e.value}s")
            await asyncio.sleep(e.value + 1)

            try:
                await msg.copy(uid)
                success += 1
            except Exception as er:
                print("Retry Fail:", uid, er)
                failed += 1

        except (UserIsBlocked, PeerIdInvalid):
            failed += 1
            try:
                await remove_user(uid)
            except:
                pass

        except Exception as e:
            print("Broadcast Error:", uid, e)
            failed += 1

        # ===== PROGRESS =====
        if total % PROGRESS_EVERY == 0:
            try:
                txt = f"{sc('broadcasting')}\n\n{sc('processed')} : {total}"
                await status.edit(txt)
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

    final = (
        f"✅ {sc('broadcast completed')}\n\n"
        f"{sc('total users')} : {total}\n"
        f"{sc('success')} : {success}\n"
        f"{sc('failed')} : {failed}\n\n"
        f"{sc('time taken')} : {taken}s"
    )

    try:
        await status.edit(final)
    except:
        pass
        
