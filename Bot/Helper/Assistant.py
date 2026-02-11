from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    PeerIdInvalid,
    UserBannedInChannel
)

from Bot import bot, user
from Bot.Helper.Font import sc


ASSISTANT_ID = None
ASSISTANT_USERNAME = None

# prevent join spam
JOINING = set()


# ================= SETUP =================
async def setup_assistant():
    global ASSISTANT_ID, ASSISTANT_USERNAME
    me = await user.get_me()
    ASSISTANT_ID = me.id
    ASSISTANT_USERNAME = me.username or "NoUsername"


# ================= ENSURE ASSISTANT =================
async def get_ass(chat_id, m):
    global ASSISTANT_ID

    if not ASSISTANT_ID:
        await setup_assistant()

    # already in chat?
    try:
        await bot.get_chat_member(chat_id, ASSISTANT_ID)
        return True
    except:
        pass

    # prevent multi join attempts
    if chat_id in JOINING:
        return False

    JOINING.add(chat_id)

    try:
        bot_id = (await bot.get_me()).id
        bot_member = await bot.get_chat_member(chat_id, bot_id)

        if not bot_member.privileges or not bot_member.privileges.can_invite_users:
            raise ChatAdminRequired

        link = await bot.export_chat_invite_link(chat_id)
        await user.join_chat(link)
        return True

    except UserAlreadyParticipant:
        return True

    except UserBannedInChannel:
        await m.reply(
            sc("assistant is banned in this group\nunban first")
        )
        return False

    except (ChatAdminRequired, PeerIdInvalid):
        await m.reply(
            sc(
                "assistant not in group\n"
                "give invite permission or add manually"
            )
            + f"\n\n@{ASSISTANT_USERNAME}\n`{ASSISTANT_ID}`"
        )
        return False

    except Exception as e:
        print("Assistant Join Error:", e)
        await m.reply(sc("failed to bring assistant"))
        return False

    finally:
        JOINING.discard(chat_id)
