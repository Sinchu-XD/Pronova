import random
from pyrogram.types import MessageEntity
from pyrogram import enums
from Bot import CUSTOM_EMOJI_IDS


SMALL_CAPS = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ",
    "f": "ғ", "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ",
    "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ", "o": "ᴏ",
    "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ",
    "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ",
    "z": "ᴢ"
}


def sc(text: str, entities: bool = False):
    if not text:
        return ""

    result = []

    for word in text.split(" "):
        if not word:
            result.append(word)
            continue

        first = word[0].upper() if word[0].isalpha() else word[0]

        rest_chars = []
        for ch in word[1:]:
            if ch.isalpha():
                rest_chars.append(SMALL_CAPS.get(ch.lower(), ch))
            else:
                rest_chars.append(ch)

        result.append(first + "".join(rest_chars))

    styled = f"**{' '.join(result)}**"

    # ===== PREMIUM PART =====
    left_id = random.choice(CUSTOM_EMOJI_IDS)
    right_id = random.choice(CUSTOM_EMOJI_IDS)

    final_text = f"❤️ {styled} ❤️"

    premium_entities = [
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=0,
            length=1,
            custom_emoji_id=left_id
        ),
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=len(final_text) - 1,
            length=1,
            custom_emoji_id=right_id
        )
    ]

    if entities:
        return final_text, premium_entities

    return final_text
