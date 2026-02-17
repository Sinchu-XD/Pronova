import random
from pyrogram import enums
from pyrogram.types import MessageEntity
from Bot import CUSTOM_EMOJI_IDS


# =====================================================
# CORE RANDOM EMOJI PICK
# =====================================================

def _get_random_id():
    return int(random.choice(CUSTOM_EMOJI_IDS))


# =====================================================
# SINGLE PREMIUM EMOJI (END OF TEXT)
# =====================================================

def add_premium(text: str):
    """
    Adds one premium emoji at the end of text
    """

    emoji_id = _get_random_id()

    # Add visible placeholder
    text = f"{text} ❤️"

    offset = len(text) - 1

    entity = MessageEntity(
        type=enums.MessageEntityType.CUSTOM_EMOJI,
        offset=offset,
        length=1,
        custom_emoji_id=emoji_id
    )

    return text, [entity]


# =====================================================
# LEFT + RIGHT PREMIUM (MULTILINE SAFE)
# =====================================================

def add_premium_lr(text: str):
    """
    Adds premium emoji on left and right of every line
    """

    lines = text.split("\n")

    final_text = ""
    entities = []
    offset = 0

    for line in lines:

        left_id = _get_random_id()
        right_id = _get_random_id()

        new_line = f"❤️ {line} ❤️"

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


# =====================================================
# MULTIPLE RANDOM EMOJIS INLINE (ADVANCED)
# =====================================================

def add_inline(text: str, count: int = 2):
    """
    Adds multiple premium emojis at the end
    """

    entities = []

    for _ in range(count):
        emoji_id = _get_random_id()
        text += " ❤️"

        entities.append(
            MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=len(text) - 1,
                length=1,
                custom_emoji_id=emoji_id
            )
        )

    return text, entities
