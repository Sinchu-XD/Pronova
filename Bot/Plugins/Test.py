import random
from pyrogram import filters, enums
from pyrogram.types import MessageEntity

from Bot import bot, CUSTOM_EMOJI_IDS


# ===== Premium Left + Right Function =====
def premium_lr(text: str):
    left_id = random.choice(CUSTOM_EMOJI_IDS)
    right_id = random.choice(CUSTOM_EMOJI_IDS)

    new_text = f"❤️ {text} ❤️"

    entities = [
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=0,
            length=1,
            custom_emoji_id=left_id
        ),
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=len(new_text) - 1,
            length=1,
            custom_emoji_id=right_id
        )
    ]

    return new_text, entities


# ===== Test Command =====
@bot.on_message(filters.command("test"))
async def test_command(_, message):
    text, ent = premium_lr("Bot Working Fine 🔥")
    await message.reply(text, entities=ent)
  
