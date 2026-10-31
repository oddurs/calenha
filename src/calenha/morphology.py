"""Building words from their parts."""

from __future__ import annotations

from collections.abc import Sequence

from .phonology import Phonology, normalize


def join(parts: Sequence[str], phonology: Phonology) -> str:
    """Join roots, words and affixes into one word.

    One soft rule applies: when a vowel-initial suffix meets a word that ends in a
    vowel, the word's last vowel gives way — ``calenha + -i → calenhi``.
    Hyphens only mark where an affix attaches; they are never spelled.
    """
    word = ""
    for part in parts:
        part = normalize(part)
        bare = part.strip("-")
        if not bare:
            continue
        if word and part.startswith("-") and _starts_vowel(bare, phonology):
            if _ends_vowel(word, phonology):
                word = word[:-1]
        word += bare
    return word


def _starts_vowel(text: str, phonology: Phonology) -> bool:
    return phonology.tokenize(text)[0].is_vowel


def _ends_vowel(text: str, phonology: Phonology) -> bool:
    return phonology.tokenize(text)[-1].is_vowel
