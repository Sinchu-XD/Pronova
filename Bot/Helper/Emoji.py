import random
from Bot import CUSTOM_EMOJI_IDS


def _get_random_id():
    return int(random.choice(CUSTOM_EMOJI_IDS))


def add_premium(text: str):
    emoji_id = _get_random_id()
    return f'{text} <emoji id="{emoji_id}"></emoji>'


def add_premium_lr(text: str):
    lines = text.split("\n")
    final = ""

    for line in lines:
        left = _get_random_id()
        right = _get_random_id()

        final += (
            f'<emoji id="{left}"></emoji> '
            f'{line} '
            f'<emoji id="{right}"></emoji>\n'
        )

    return final.rstrip("\n")
