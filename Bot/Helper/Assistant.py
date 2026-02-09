from pyrogram.errors import ChatAdminRequired, UserAlreadyParticipant, PeerIdInvalid
from Bot import bot, user
from Bot.Helper.Font import sc

ASSISTANT_ID = None
ASSISTANT_USERNAME = None


async def setup_assistant():
    global ASSISTANT_ID, ASSISTANT_USERNAME
    me = await user.get_me()
    ASSISTANT_ID = me.id
    ASSISTANT_USERNAME = me.username or "NoUsername"


async def get_ass(chat_id, m):
    try:
        await bot.get_chat_member(chat_id, ASSISTANT_ID)
        return True
    except:
        pass

    try:
        bot_member = await bot.get_chat_member(chat_id, (await bot.get_me()).id)

        if not bot_member.privileges or not bot_member.privileges.can_invite_users:
            raise ChatAdminRequired

        link = await bot.export_chat_invite_link(chat_id)
        await user.join_chat(link)
        return True

    except UserAlreadyParticipant:
        return True

    except (ChatAdminRequired, PeerIdInvalid):
        await m.reply(
            sc(
                "assistant not in group\n"
                "give invite permission or add manually"
            )
            + f"\n\n@{ASSISTANT_USERNAME}\n`{ASSISTANT_ID}`"
        )
        return False
      
