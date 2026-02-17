import random
from pyrogram import enums
from pyrogram.types import MessageEntity
from Bot import CUSTOM_EMOJI_IDS


def add_random_emoji(text: str):
    emoji_id = int(random.choice(CUSTOM_EMOJI_IDS))

    text = f"{text} ❤️"
    offset = len(text) - 1

    entity = MessageEntity(
        type=enums.MessageEntityType.CUSTOM_EMOJI,
        offset=offset,
        length=1,
        custom_emoji_id=emoji_id
    )

    return text, [entity]
  
