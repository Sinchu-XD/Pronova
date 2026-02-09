SMALL_CAPS = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ",
    "f": "ғ", "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ",
    "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ", "o": "ᴏ",
    "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ",
    "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ",
    "z": "ᴢ"
}


def sc(text: str) -> str:
    words = text.split(" ")
    final = []

    for word in words:
        if not word:
            final.append(word)
            continue

        first = word[0].upper()
        rest = ""

        for ch in word[1:]:
            rest += SMALL_CAPS.get(ch.lower(), ch)

        final.append(first + rest)

    return " ".join(final)
  
