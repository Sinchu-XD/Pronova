SMALL_CAPS = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ",
    "f": "ғ", "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ",
    "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ", "o": "ᴏ",
    "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ",
    "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ",
    "z": "ᴢ"
}


def sc(text: str) -> str:
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

    return f"**{' '.join(result)}**"
