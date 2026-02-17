import random
from pyrogram.types import MessageEntity
from pyrogram import enums
from Bot import CUSTOM_EMOJI_IDS


def add_premium(text: str):

    emoji_id = int(random.choice(CUSTOM_EMOJI_IDS))

    # Single ASCII placeholder
    placeholder = "•"

    new_text = f"{text} {placeholder}"

    entity = MessageEntity(
        type=enums.MessageEntityType.CUSTOM_EMOJI,
        offset=len(new_text) - 1,
        length=1,
        custom_emoji_id=emoji_id
    )

    return new_text, [entity]
