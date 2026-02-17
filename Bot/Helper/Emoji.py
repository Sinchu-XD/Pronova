import random
from pyrogram import enums
from pyrogram.types import MessageEntity
from Bot import CUSTOM_EMOJI_IDS


def _get_random_id():
    return int(random.choice(CUSTOM_EMOJI_IDS))


# ================= SINGLE PREMIUM =================
def add_premium(text: str):

    emoji_id = _get_random_id()

    # Use simple safe placeholder
    placeholder = "X"

    new_text = f"{text} {placeholder}"

    entity = MessageEntity(
        type=enums.MessageEntityType.CUSTOM_EMOJI,
        offset=len(new_text) - 1,
        length=1,
        custom_emoji_id=emoji_id
    )

    return new_text, [entity]


# ================= LEFT RIGHT PREMIUM =================
def add_premium_lr(text: str):

    lines = text.split("\n")

    final_text = ""
    entities = []
    offset = 0

    for line in lines:

        left_id = _get_random_id()
        right_id = _get_random_id()

        placeholder_left = "L"
        placeholder_right = "R"

        new_line = f"{placeholder_left} {line} {placeholder_right}"

        final_text += new_line + "\n"

        # LEFT
        entities.append(
            MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset,
                length=1,
                custom_emoji_id=left_id
            )
        )

        # RIGHT
        entities.append(
            MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset + len(new_line) - 1,
                length=1,
                custom_emoji_id=right_id
            )
        )

        offset += len(new_line) + 1

    final_text = final_text.rstrip("\n")

    return final_text, entities
    
