print("BROADCAST PLUGIN LOADED")

import asyncio
import time
import random
from pyrogram import filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.types import MessageEntity

from Bot import bot, CUSTOM_EMOJI_IDS
from Bot.Helper.Font import sc
from Bot.Database.Users import get_users, remove_user
from Bot.Database.Chats import get_all_chats
from Bot.Database.Stats import inc_lifetime
from Bot.Database.Core import db


SUDO_USERS = [7952773964]

DELAY = 0.25
PROGRESS_EVERY = 200


# ================= EMOJI HELPER =================
def add_random_emoji(text: str):
    emoji_id = random.choice(CUSTOM_EMOJI_IDS)

    text = text + " ❤️"

    entity = MessageEntity(
        type=enums.MessageEntityType.CUSTOM_EMOJI,
        offset=len(text) - 1,
        length=1,
        custom_emoji_id=emoji_id
    )

    return text, [entity]


@bot.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast(_, message):

    if not message.reply_to_message:
        text, ent = add_random_emoji("Reply to a message to broadcast.")
        return await message.reply(text, entities=ent)

    start_time = time.time()
    msg = message.reply_to_message

    total = 0
    success = 0
    failed = 0

    start_text, ent = add_random_emoji(sc("broadcast started..."))
    status = await message.reply(start_text, entities=ent)

    # ================= USERS =================
    async for user_id in get_users():
        total += 1
        uid = int(user_id)

        try:
            await msg.copy(uid)
            success += 1
            await asyncio.sleep(DELAY)

        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            try:
                await msg.copy(uid)
                success += 1
            except:
                failed += 1

        except (UserIsBlocked, PeerIdInvalid):
            failed += 1
            try:
                await remove_user(uid)
            except:
                pass

        except:
            failed += 1

        if total % PROGRESS_EVERY == 0:
            try:
                txt = f"{sc('broadcasting')}\n\n{sc('processed')} : {total}"
                txt, ent = add_random_emoji(txt)
                await status.edit(txt, entities=ent)
            except:
                pass

    # ================= GROUPS =================
    async for chat_id in get_all_chats():
        total += 1
        cid = int(chat_id)

        try:
            await msg.copy(cid)
            success += 1
            await asyncio.sleep(DELAY)

        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            try:
                await msg.copy(cid)
                success += 1
            except:
                failed += 1

        except:
            failed += 1

        if total % PROGRESS_EVERY == 0:
            try:
                txt = f"{sc('broadcasting')}\n\n{sc('processed')} : {total}"
                txt, ent = add_random_emoji(txt)
                await status.edit(txt, entities=ent)
            except:
                pass

    # ================= LOG =================
    try:
        await db.broadcasts.insert_one({
            "total": total,
            "success": success,
            "failed": failed,
            "time": int(time.time())
        })
    except:
        pass

    await inc_lifetime("broadcasts")

    taken = round(time.time() - start_time, 2)

    final = (
        f"✅ {sc('broadcast completed')}\n\n"
        f"{sc('total targets')} : {total}\n"
        f"{sc('success')} : {success}\n"
        f"{sc('failed')} : {failed}\n\n"
        f"{sc('time taken')} : {taken}s"
    )

    final, ent = add_random_emoji(final)

    try:
        await status.edit(final, entities=ent)
    except:
        pass
        
