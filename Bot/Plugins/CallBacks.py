from pyrogram.enums import ChatMemberStatus

from Bot import bot, engine
from Bot.Helper.Font import sc
from Bot.Helper.Emoji import add_premium
from Bot.Database.Bans import is_banned, is_gbanned


# ================= SAFE VC =================
async def safe_action(action, chat_id):
    try:
        return await action(chat_id)
    except Exception as e:
        print("Callback VC Error:", e)
        return None


# ================= ADMIN CHECK =================
async def is_admin(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        )
    except:
        return False


@bot.on_callback_query()
async def vc_buttons(_, cq):
    try:
        if not cq.message:
            return await cq.answer()

        m = cq.message
        chat_id = m.chat.id
        user = cq.from_user

        if not user or user.is_bot:
            return await cq.answer()

        uid = user.id

        # ================= BAN CHECK =================
        if await is_gbanned(uid):
            return await cq.answer(sc("you are gbanned"), show_alert=True)

        if await is_banned(chat_id, uid):
            return await cq.answer(sc("you are banned in this chat"), show_alert=True)

        # ================= ADMIN CHECK =================
        if not await is_admin(chat_id, uid):
            return await cq.answer(sc("admins only"), show_alert=True)

        mention = user.mention

        # ================= ACTIONS =================
        if cq.data == "vc_skip":
            await safe_action(engine.vc.skip, chat_id)
            text, ent = add_premium(sc("song skipped by") + " " + mention)
            await m.reply(text, entities=ent)

        elif cq.data == "vc_end":
            await safe_action(engine.vc.stop, chat_id)
            text, ent = add_premium(sc("playback ended by") + " " + mention)
            await m.reply(text, entities=ent)

        elif cq.data == "vc_pause":
            await safe_action(engine.vc.pause, chat_id)
            text, ent = add_premium(sc("paused by") + " " + mention)
            await m.reply(text, entities=ent)

        elif cq.data == "vc_resume":
            await safe_action(engine.vc.resume, chat_id)
            text, ent = add_premium(sc("resumed by") + " " + mention)
            await m.reply(text, entities=ent)

        elif cq.data == "vc_previous":
            ok = await safe_action(engine.vc.previous, chat_id)
            if not ok:
                text, ent = add_premium(sc("no previous song"))
                await m.reply(text, entities=ent)

        else:
            return await cq.answer()

        await cq.answer()

    except Exception as e:
        print("Callback Fatal Error:", e)
        try:
            await cq.answer("Error", show_alert=True)
        except:
            pass
            
