def sc(text: str):
    if not text:
        return ""

    words = []

    for word in text.split(" "):
        if not word:
            words.append(word)
            continue

        first = word[0].upper() if word[0].isalpha() else word[0]

        rest = []
        for ch in word[1:]:
            if ch.isalpha():
                rest.append(SMALL_CAPS.get(ch.lower(), ch))
            else:
                rest.append(ch)

        words.append(first + "".join(rest))

    return ' '.join(words)
