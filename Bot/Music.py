import os
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserAlreadyParticipant, PeerIdInvalid
from pyrogram.enums import ChatMemberStatus
from AbhiCalls import VoiceEngine, idle, Plugin
# ───────── CONFIG ─────────
API_ID = 35362137
API_HASH = "c3c3e167ea09bc85369ca2fa3c1be790"
BOT_TOKEN = "8490783791:AAFT8DygQAO5cC-Bg6yi_D-0c7wOlIKDFdA"
SESSION_STRING = "BQBclYcAZZe_0_YNC3mOH2z2HnljeghVhYJtdRbsF7MgU7gBoqbKX0_W5HJdj4ba_gvGyEwKrkegiU6hJ38XjoIaIA69urDjjYZkWnzYtWdUcgeQkM0eKmCKanPdhz6Eqkg0D8s1kznoIFhW4T5N6yQ6DcXW7Q04GFEJRsNMSmPtNMdWWP_LXrb-WcpY4dvCkamUOw7ICqw4DPWXjtGdc36UHeClVy-DYmdVZfgipCZ50f7Mir>
ASSISTANT_ID = None
ASSISTANT_USERNAME = None
# 🤖 Bot
bot = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# 👤 Assistant
user = Client("music_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
engine = VoiceEngine(user)
# ───────── ASSISTANT INFO ─────────
async def fetch_assistant():
    global ASSISTANT_ID, ASSISTANT_USERNAME
    me = await user.get_me()
    ASSISTANT_ID = me.id
    ASSISTANT_USERNAME = me.username or "NoUsername"
# ───────── ENSURE ASSISTANT ─────────
async def ensure_assistant(bot, user, chat_id, m):
    try:
        await bot.get_chat_member(chat_id, ASSISTANT_ID)
        return True
    except:
        pass
    try:
        bot_member = await bot.get_chat_member(chat_id, bot.me.id)
        if not bot_member.privileges or not bot_member.privileges.can_invite_users:
            raise ChatAdminRequired
        invite = await bot.export_chat_invite_link(chat_id)
        await user.join_chat(invite)
        return True
    except UserAlreadyParticipant:
        return True
    except (ChatAdminRequired, PeerIdInvalid):
        await m.reply(
            "Aꜱꜱɪꜱᴛᴀɴᴛ Nᴏᴛ Iɴ Tʜɪꜱ Gʀᴏᴜᴘ\n\n"
            "Gɪᴠᴇ Iɴᴠɪᴛᴇ Pᴇʀᴍɪꜱꜱɪᴏɴ Oʀ Aᴅᴅ Mᴀɴᴜᴀʟʟʏ\n\n"
            f"@{ASSISTANT_USERNAME}\n"
            f"ID: `{ASSISTANT_ID}`"
        )
        return False
# ───────── PLAY ─────────
@bot.on_message(filters.command("play"))
async def play(_, m):
    try:
        await m.delete()
    except:
        pass
    if not await ensure_assistant(bot, user, m.chat.id, m):
        return
    reply = m.reply_to_message
    if reply and (reply.voice or reply.audio):
        path = await reply.download()
        song, _ = await engine.vc.play_file(m.chat.id, path, m.from_user.mention, reply=reply)
        if not song:
            await m.reply("Uɴᴀʙʟᴇ Tᴏ Pʟᴀʏ Aᴜᴅɪᴏ")
        return
    if len(m.command) < 2:
        return await m.reply("Uꜱᴀɢᴇ: /ᴘʟᴀʏ ꜱᴏɴɢ ɴᴀᴍᴇ")
    query = m.text.split(None, 1)[1]
    song, _ = await engine.vc.play(m.chat.id, query, m.from_user.mention)
    if not song:
        await m.reply("Uɴᴀʙʟᴇ Tᴏ Pʟᴀʏ Sᴏɴɢ")
# ───────── PLAYFORCE ─────────
@bot.on_message(filters.command("playforce"))
async def playforce(_, m):
    try:
        await m.delete()
    except:
        pass
    if not await ensure_assistant(bot, user, m.chat.id, m):
        return
    await engine.vc.stop(m.chat.id)
    reply = m.reply_to_message
    if reply and (reply.voice or reply.audio):
        path = await reply.download()
        song, _ = await engine.vc.play_file(m.chat.id, path, m.from_user.mention, reply=reply)
        if not song:
            await m.reply("Uɴᴀʙʟᴇ Tᴏ Fᴏʀᴄᴇ Pʟᴀʏ")
        return
    if len(m.command) < 2:
        return await m.reply("Uꜱᴀɢᴇ: /ᴘʟᴀʏꜰᴏʀᴄᴇ ꜱᴏɴɢ")
    query = m.text.split(None, 1)[1]
    await engine.vc.play(m.chat.id, query, m.from_user.mention)
# ───────── CALLBACK BUTTONS ─────────
@bot.on_callback_query()
async def vc_buttons(_, cq):
    m = cq.message
    chat_id = m.chat.id
    member = await bot.get_chat_member(chat_id, cq.from_user.id)
    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        return await cq.answer("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Uꜱᴇ Tʜɪꜱ!", show_alert=True)
    if cq.data == "vc_skip":
        await engine.vc.skip(chat_id)
        await m.reply(f"Sᴋɪᴘᴘᴇᴅ Bʏ {cq.from_user.mention}")
    elif cq.data == "vc_end":
        await engine.vc.stop(chat_id)
        await m.reply(f"Eɴᴅᴇᴅ Bʏ {cq.from_user.mention}")
    elif cq.data == "vc_pause":
        await engine.vc.pause(chat_id)
        await m.reply(f"Pᴀᴜꜱᴇᴅ Bʏ {cq.from_user.mention}")
    elif cq.data == "vc_resume":
        await engine.vc.resume(chat_id)
        await m.reply(f"Rᴇꜱᴜᴍᴇᴅ Bʏ {cq.from_user.mention}")
    elif cq.data == "vc_previous":
        ok = await engine.vc.previous(chat_id)
        if not ok:
            await m.reply("Nᴏ Pʀᴇᴠɪᴏᴜꜱ Sᴏɴɢ")
    await cq.answer()
# ───────── ADMIN COMMANDS ─────────
async def _is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
# ───────── SKIP ─────────
@bot.on_message(filters.command("skip"))
async def skip(_, m):
    if not await _is_admin(m.chat.id, m.from_user.id):
        return await m.reply("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Sᴋɪᴘ")
    await engine.vc.skip(m.chat.id)
    await m.reply(f"Sᴏɴɢ Sᴋɪᴘᴘᴇᴅ Bʏ {m.from_user.mention}")
# ───────── END / STOP ─────────
@bot.on_message(filters.command(["end", "stop"]))
async def stop(_, m):
    if not await _is_admin(m.chat.id, m.from_user.id):
        return await m.reply("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Eɴᴅ")
    await engine.vc.stop(m.chat.id)
    await m.reply(f"Pʟᴀʏʙᴀᴄᴋ Eɴᴅᴇᴅ Bʏ {m.from_user.mention}")
# ───────── PAUSE ─────────
@bot.on_message(filters.command("pause"))
async def pause(_, m):
    if not await _is_admin(m.chat.id, m.from_user.id):
        return await m.reply("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Pᴀᴜꜱᴇ")
    await engine.vc.pause(m.chat.id)
    await m.reply(f"Pᴀᴜꜱᴇᴅ Bʏ {m.from_user.mention}")
  # ───────── RESUME ─────────
@bot.on_message(filters.command("resume"))
async def resume(_, m):
    if not await _is_admin(m.chat.id, m.from_user.id):
        return await m.reply("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Rᴇꜱᴜᴍᴇ")
    await engine.vc.resume(m.chat.id)
    await m.reply(f"Rᴇꜱᴜᴍᴇᴅ Bʏ {m.from_user.mention}")
# ───────── PREVIOUS ─────────
@bot.on_message(filters.command("previous"))
async def previous(_, m):
    if not await _is_admin(m.chat.id, m.from_user.id):
        return await m.reply("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Pʟᴀʏ Pʀᴇᴠɪᴏᴜꜱ")
    song = await engine.vc.previous(m.chat.id)
    if not song:
        return await m.reply("Nᴏ Pʀᴇᴠɪᴏᴜꜱ Sᴏɴɢ")
    await m.reply(f"Pʀᴇᴠɪᴏᴜꜱ Pʟᴀʏᴇᴅ Bʏ {m.from_user.mention}")
# ───────── QUEUE ─────────
@bot.on_message(filters.command("queue"))
async def queue(_, m):
    if not await _is_admin(m.chat.id, m.from_user.id):
        return await m.reply("Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Vɪᴇᴡ Qᴜᴇᴜᴇ")
    q = engine.vc.player.queues.get(m.chat.id)
    if not q or not q.items:
        return await m.reply("Qᴜᴇᴜᴇ Iꜱ Eᴍᴘᴛʏ")
    text = "Qᴜᴇᴜᴇ Lɪꜱᴛ\n\n"
    for i, s in enumerate(q.items, 1):
        text += f"{i}. {s.title} ({s.duration_sec}s)\n"
    await m.reply(text)
# ───────── MAIN ─────────
async def main():
    # ENV (Powered by button)
    os.environ["TEXT"] =  "Pᴏᴡᴇʀᴇᴅ Bʏ 𝐀ʙʜɪsʜᴇᴋ ✨ "
    os.environ["LINK"] = "https://t.me/Her4Eva"
    await bot.start()
    await user.start()
    await engine.start()
    await fetch_assistant()
    engine.vc.load_plugin(Plugin(bot))
    await idle()
bot.run(main())
