"""Coining words: sample from the sound system, then listen.

The generator proposes many words that obey the phonology, scores each for
euphony, and returns the most beautiful. Its taste lives in the ``[euphony]``
table of ``lang/phonology.toml``. It proposes; a person chooses.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import pairwise

from .language import Language
from .phonology import Kind, Phonology, PhonologyError, Word


@dataclass(frozen=True)
class Candidate:
    word: Word
    score: float
    echoes: tuple[str, ...]  # existing words within one letter


def tiers(phonology: Phonology) -> dict[str, float]:
    """How welcome each consonant is to the ear, from ``[euphony.tiers]``."""
    welcome: dict[str, float] = {}
    for tier in phonology.spec.get("euphony", {}).get("tiers", {}).values():
        for sound in tier["sounds"]:
            welcome[sound] = tier["weight"]
    return welcome


def euphony(word: Word, phonology: Phonology) -> float:
    """A 0–1 judgement of how a word sounds: soft, open, varied and unhurried."""
    welcome = tiers(phonology)
    syllables = word.syllables
    consonants = [s for s in word.sounds if not s.is_vowel]

    softness = (
        sum(welcome.get(c.text, 0.5) for c in consonants) / len(consonants) if consonants else 0.7
    )
    openness = sum(syl.is_open for syl in syllables) / len(syllables)
    vowels = {syl.nucleus.text for syl in syllables}
    variety = min(1.0, len(vowels) / max(1, len(syllables) - 0.5))
    length = {1: 0.7, 2: 0.95, 3: 1.0, 4: 0.9}.get(len(syllables), 0.6)

    rhythm = 1.0
    pairs = list(pairwise(syllables))
    rhythm -= 0.3 * sum(not b.onset for _, b in pairs)  # vowels colliding
    rhythm -= 0.3 * sum(  # the same sound twice running: chechë
        bool(a.onset and b.onset and a.onset[0].text == b.onset[0].text) for a, b in pairs
    )
    rhythm -= 0.25 * max(0, sum(s.nucleus.kind is Kind.DIPHTHONG for s in syllables) - 1)
    rhythm -= 0.3 * max(0, sum(len(s.onset) > 1 for s in syllables) - 1)
    rhythm = max(0.0, rhythm)

    score = 0.35 * softness + 0.2 * openness + 0.15 * variety + 0.15 * length + 0.15 * rhythm
    if any(a.text == b.text for a, b in pairs):
        score *= 0.6  # stammering
    last = syllables[-1].nucleus
    if last.kind is Kind.NASAL or last.text == "ë":
        score += 0.03  # a little lift at the end
    return round(max(0.0, min(1.0, score)), 3)


def generate(
    language: Language,
    n: int = 12,
    syllables: tuple[int, int] = (2, 3),
    kind: str = "noun",
    seed: int | None = None,
    attempts: int = 600,
) -> list[Candidate]:
    """The ``n`` most euphonious new words from ``attempts`` tries.

    ``kind`` is ``noun`` (never ends in -u), ``verb`` (always does) or ``any``.
    """
    rng = random.Random(seed)
    phonology = language.phonology
    existing = {e.word for e in language.entries}
    found: dict[str, Candidate] = {}

    for _ in range(attempts):
        text = _sample(phonology, rng, rng.randint(*syllables), kind)
        if text in existing or text in found or phonology.problems(text):
            continue
        try:
            word = phonology.syllabify(text)
        except PhonologyError:
            continue
        echoes = tuple(sorted(w for w in existing if _near(w, text)))
        found[text] = Candidate(word, euphony(word, phonology), echoes)

    pool = list(found.values())
    rng.shuffle(pool)  # equal scores come out in a fresh order each seed
    return sorted(pool, key=lambda c: -c.score)[:n]


def _sample(phonology: Phonology, rng: random.Random, count: int, kind: str) -> str:
    taste = phonology.spec.get("euphony", {})
    welcome = tiers(phonology)
    consonants = [c.text for c in phonology.consonants]
    weights = [welcome.get(c, 0.5) ** 2 for c in consonants]
    clusters = ["".join(c) for c in sorted(phonology.clusters)]
    vowel_weights = taste.get("vowel_weights", {})
    plain = list(vowel_weights) or ["a", "e", "i", "o", "u"]
    plain_w = [vowel_weights.get(v, 1) for v in plain]
    diphthongs = [s.text for s in phonology.of_kind(Kind.DIPHTHONG)]
    nasals = [s.text for s in phonology.of_kind(Kind.NASAL)]
    longs = [s.text for s in phonology.of_kind(Kind.LONG)]

    parts: list[str] = []
    has_long = False
    for i in range(count):
        first, last = i == 0, i == count - 1

        roll = rng.random()
        if roll < (0.2 if first else 0.08):
            onset = ""
        elif roll < 0.3:
            onset = rng.choice(clusters)
        else:
            onset = rng.choices(consonants, weights)[0]
            while first and onset in phonology.not_initial:
                onset = rng.choices(consonants, weights)[0]

        roll = rng.random()
        nasal = False
        if last and kind == "verb":
            nucleus = "u"
        elif roll < 0.04 and not has_long and not last:
            nucleus, has_long = rng.choice(longs), True
        elif roll < 0.15:
            # a final glide in -u would read as a verb
            glides = [d for d in diphthongs if not (last and d.endswith("u"))]
            nucleus = rng.choice(glides)
        elif last and roll < 0.24:
            nucleus, nasal = rng.choice(nasals), True
        else:
            nucleus = rng.choices(plain, plain_w)[0]
            while last and kind == "noun" and nucleus == "u":
                nucleus = rng.choices(plain, plain_w)[0]

        coda = ""
        if last:
            if kind != "verb" and not nasal and rng.random() < 0.25:
                coda = rng.choice(sorted(phonology.final_codas))
            elif nucleus == "e":
                nucleus = "ë"
        elif rng.random() < 0.2:
            coda = rng.choice(sorted(phonology.codas))

        parts.append(onset + nucleus + coda)
    return "".join(parts)


def _near(a: str, b: str) -> bool:
    """Within one edit of each other."""
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b, strict=True)) <= 1
    short, long_ = sorted((a, b), key=len)
    return any(long_[:i] + long_[i + 1 :] == short for i in range(len(long_)))
