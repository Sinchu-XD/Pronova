from pyrogram.enums import ChatMemberStatus
from Bot import bot, engine
from Bot.Helper.Font import sc


@bot.on_callback_query()
async def vc_buttons(_, cq):
    m = cq.message
    chat_id = m.chat.id

    member = await bot.get_chat_member(chat_id, cq.from_user.id)
    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        return await cq.answer(sc("only admins"), show_alert=True)

    mention = cq.from_user.mention

    if cq.data == "vc_skip":
        await engine.vc.skip(chat_id)
        await m.reply(sc("song skipped by") + " " + mention)

    elif cq.data == "vc_end":
        await engine.vc.stop(chat_id)
        await m.reply(sc("playback ended by") + " " + mention)

    elif cq.data == "vc_pause":
        await engine.vc.pause(chat_id)
        await m.reply(sc("paused by") + " " + mention)

    elif cq.data == "vc_resume":
        await engine.vc.resume(chat_id)
        await m.reply(sc("resumed by") + " " + mention)

    elif cq.data == "vc_previous":
        ok = await engine.vc.previous(chat_id)
        if not ok:
            await m.reply(sc("no previous song"))

    await cq.answer()
