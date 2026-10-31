"""Sound change: running Old Calenha forward into the modern language.

Each change in ``lang/sound-changes.toml`` is a rewrite with an environment written
the way linguists write it: ``_`` is the sound itself, ``V`` any vowel, ``C`` any
consonant, ``#`` the edge of the word. ``when = "l_"`` means "after l".
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .language import Language, SoundChange
from .phonology import Kind, normalize


@dataclass(frozen=True)
class Step:
    change: SoundChange
    before: str
    after: str


@dataclass(frozen=True)
class Evolution:
    old: str
    word: str
    steps: tuple[Step, ...]


def evolve(old: str, language: Language) -> Evolution:
    """Apply every sound change, in order, recording the ones that did something."""
    word = normalize(old).lstrip("*")
    steps = []
    vowels = _vowel_letters(language)
    for change in language.sound_changes:
        pattern, table = _compile(change, vowels)
        result = pattern.sub(lambda m, table=table: table[m.group(0)], word)
        if result != word:
            steps.append(Step(change, word, result))
            word = result
    return Evolution(normalize(old).lstrip("*"), word, tuple(steps))


def _vowel_letters(language: Language) -> str:
    letters = {
        ch
        for sound in language.phonology.sounds.values()
        if sound.kind is not Kind.CONSONANT
        for ch in sound.text
    }
    return "".join(sorted(letters))


def _compile(change: SoundChange, vowels: str) -> tuple[re.Pattern[str], dict[str, str]]:
    table = dict(change.pairs) if change.pairs else {change.find: change.replace}
    table = {normalize(k): normalize(v) for k, v in table.items()}
    target = "|".join(re.escape(k) for k in sorted(table, key=len, reverse=True))

    left, _, right = (change.when or "_").partition("_")
    vowel = f"[{re.escape(vowels)}]"
    consonant = f"[^{re.escape(vowels)}\\W\\d_]"

    def env(text: str, edge: str) -> str:
        out = []
        for ch in text:
            if ch == "V":
                out.append(vowel)
            elif ch == "C":
                out.append(consonant)
            elif ch == "#":
                out.append(edge)
            else:
                out.append(re.escape(normalize(ch)))
        return "".join(out)

    pattern = f"(?<={env(left, '^')})" if left else ""
    pattern += f"(?:{target})"
    pattern += f"(?={env(right, '$')})" if right else ""
    return re.compile(pattern), table
