import random
from Bot import CUSTOM_EMOJI_IDS


def _get_random_id():
    return int(random.choice(CUSTOM_EMOJI_IDS))


def add_premium(text: str):
    emoji_id = _get_random_id()
    emoji_tag = f'<emoji id="{emoji_id}"></emoji>'
    return f"{text} {emoji_tag}", None


def add_premium_lr(text: str):
    lines = text.split("\n")
    final = ""

    for line in lines:
        left_id = _get_random_id()
        right_id = _get_random_id()

        left = f'<emoji id="{left_id}"></emoji>'
        right = f'<emoji id="{right_id}"></emoji>'

        final += f"{left} {line} {right}\n"

    return final.rstrip("\n"), None
    
