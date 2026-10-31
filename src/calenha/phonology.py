"""The sound system: spelling, syllables, stress and pronunciation.

Everything here is driven by ``lang/phonology.toml``. The module turns a written word
into sounds, sounds into syllables, picks the stressed syllable, and renders IPA.
"""

from __future__ import annotations

import tomllib
import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

BREATH = "·"


class Kind(Enum):
    VOWEL = "vowel"
    LONG = "long"
    NASAL = "nasal"
    DIPHTHONG = "diphthong"
    CONSONANT = "consonant"

    @property
    def is_vowel(self) -> bool:
        return self is not Kind.CONSONANT


@dataclass(frozen=True)
class Sound:
    """One grapheme and the sound it stands for."""

    text: str
    kind: Kind
    ipa: str

    @property
    def is_vowel(self) -> bool:
        return self.kind.is_vowel


@dataclass(frozen=True)
class Syllable:
    onset: tuple[Sound, ...]
    nucleus: Sound
    coda: tuple[Sound, ...]

    @property
    def sounds(self) -> tuple[Sound, ...]:
        return (*self.onset, self.nucleus, *self.coda)

    @property
    def text(self) -> str:
        return "".join(s.text for s in self.sounds)

    @property
    def is_open(self) -> bool:
        return not self.coda


@dataclass(frozen=True)
class Word:
    """A written word, broken into syllables, with its stress found."""

    text: str
    syllables: tuple[Syllable, ...]
    stress: int

    @property
    def sounds(self) -> tuple[Sound, ...]:
        return tuple(s for syl in self.syllables for s in syl.sounds)

    def hyphenated(self, mark: str = "·") -> str:
        """``tha·LÍ·rë`` — syllables apart, the stressed one raised."""
        parts = [
            syl.text.upper() if i == self.stress and len(self.syllables) > 1 else syl.text
            for i, syl in enumerate(self.syllables)
        ]
        return mark.join(parts)

    def ipa(self) -> str:
        return _render_ipa(self)


class PhonologyError(ValueError):
    """A word that the sound system cannot pronounce."""

    def __init__(self, word: str, reason: str):
        super().__init__(f"{word!r}: {reason}")
        self.word = word
        self.reason = reason


def normalize(text: str) -> str:
    """Compose accents and lowercase — capitals are grammar, not spelling."""
    return unicodedata.normalize("NFC", text).lower()


class Phonology:
    """The sound system, as described by ``phonology.toml``."""

    def __init__(self, spec: dict):
        self.spec = spec
        self.sounds: dict[str, Sound] = {}
        for table, kind in (
            ("vowels", Kind.VOWEL),
            ("long_vowels", Kind.LONG),
            ("nasals", Kind.NASAL),
            ("diphthongs", Kind.DIPHTHONG),
            ("consonants", Kind.CONSONANT),
        ):
            for grapheme, ipa in spec[table].items():
                key = normalize(grapheme)
                if key in self.sounds:
                    raise ValueError(f"grapheme {key!r} is defined twice")
                self.sounds[key] = Sound(key, kind, ipa)
        self._longest = max(len(g) for g in self.sounds)

        syllable = spec["syllable"]
        self.not_initial = frozenset(syllable["not_initial"])
        self.codas = frozenset(syllable["codas"])
        self.final_codas = frozenset(syllable["final_codas"])
        self.clusters = frozenset(
            tuple(s.text for s in self.tokenize(c)) for c in syllable["clusters"]
        )

    @classmethod
    def load(cls, path: Path) -> Phonology:
        with path.open("rb") as f:
            return cls(tomllib.load(f))

    # -- inventory ---------------------------------------------------------------

    def of_kind(self, *kinds: Kind) -> list[Sound]:
        return [s for s in self.sounds.values() if s.kind in kinds]

    @property
    def consonants(self) -> list[Sound]:
        return self.of_kind(Kind.CONSONANT)

    # -- reading -----------------------------------------------------------------

    def tokenize(self, word: str) -> list[Sound]:
        """Split a word into sounds, longest grapheme first (``nh`` before ``n``)."""
        text = normalize(word)
        out: list[Sound] = []
        i = 0
        while i < len(text):
            for size in range(self._longest, 0, -1):
                piece = text[i : i + size]
                if piece in self.sounds:
                    out.append(self.sounds[piece])
                    i += size
                    break
            else:
                raise PhonologyError(word, f"{text[i]!r} is not a letter of Calenha")
        return out

    def syllabify(self, word: str) -> Word:
        """Break a word into syllables and find its stress.

        Consonants between vowels go to the following syllable when they can begin
        one (the onset is as large as it may be), and what is left closes the
        syllable before.
        """
        text = normalize(word).replace(BREATH, "")
        sounds = self.tokenize(text)
        nuclei = [i for i, s in enumerate(sounds) if s.is_vowel]
        if not nuclei:
            raise PhonologyError(word, "a word needs at least one vowel")

        first, last = nuclei[0], nuclei[-1]
        onset = tuple(sounds[:first])
        if not self._is_onset(onset, initial=True):
            raise PhonologyError(word, f"cannot begin with {_spell(onset)!r}")
        final = tuple(sounds[last + 1 :])
        if len(final) > 1 or (final and final[0].text not in self.final_codas):
            raise PhonologyError(word, f"cannot end with {_spell(final)!r}")

        syllables: list[Syllable] = []
        for here, there in zip(nuclei, [*nuclei[1:], None], strict=True):
            if there is None:
                syllables.append(Syllable(onset, sounds[here], final))
                break
            between = tuple(sounds[here + 1 : there])
            coda, next_onset = self._split(word, between)
            syllables.append(Syllable(onset, sounds[here], coda))
            onset = next_onset

        return Word(text, tuple(syllables), self._stress(word, syllables))

    def _is_onset(self, cluster: tuple[Sound, ...], *, initial: bool = False) -> bool:
        if len(cluster) == 0:
            return True
        if len(cluster) == 1:
            return not (initial and cluster[0].text in self.not_initial)
        return tuple(s.text for s in cluster) in self.clusters

    def _split(
        self, word: str, between: tuple[Sound, ...]
    ) -> tuple[tuple[Sound, ...], tuple[Sound, ...]]:
        for k in range(len(between) + 1):
            coda, onset = between[:k], between[k:]
            coda_ok = len(coda) == 0 or (len(coda) == 1 and coda[0].text in self.codas)
            if coda_ok and self._is_onset(onset):
                return coda, onset
        raise PhonologyError(word, f"{_spell(between)!r} cannot sit between two vowels")

    def _stress(self, word: str, syllables: list[Syllable]) -> int:
        long = [i for i, s in enumerate(syllables) if s.nucleus.kind is Kind.LONG]
        if len(long) > 1:
            raise PhonologyError(word, "only one vowel in a word may be long")
        if long:
            return long[0]
        if syllables[-1].nucleus.kind is Kind.NASAL and not syllables[-1].coda:
            return len(syllables) - 1
        return max(0, len(syllables) - 2)

    # -- judging -----------------------------------------------------------------

    def problems(self, word: str) -> list[str]:
        """Everything wrong with a word's spelling, as plain sentences. Empty is good."""
        try:
            analysed = self.syllabify(word)
        except PhonologyError as e:
            return [e.reason]
        found = []
        sounds = analysed.sounds
        for i, s in enumerate(sounds):
            at_end = i == len(sounds) - 1
            if s.text == "ë" and not at_end:
                found.append("ë may only end a word")
            if s.text == "e" and at_end:
                found.append("a final e is written ë")
        return found


def _spell(sounds: tuple[Sound, ...]) -> str:
    return "".join(s.text for s in sounds)


def _render_ipa(word: Word) -> str:
    """Broad IPA, with the soft rules of connected sound applied.

    - a single s between vowels is voiced: [z]
    - a doubled consonant across a syllable break is said once (rr becomes a trill)
    """
    syllables = word.syllables
    out = []
    for i, syl in enumerate(syllables):
        prev = syllables[i - 1] if i > 0 else None
        nxt = syllables[i + 1] if i + 1 < len(syllables) else None

        onset = [s.ipa for s in syl.onset]
        if prev and not prev.coda and [s.text for s in syl.onset] == ["s"]:
            onset = ["z"]
        elif prev and _doubled(prev, syl) and syl.onset[0].text == "r":
            onset[0] = "r"

        coda = [s.ipa for s in syl.coda]
        if nxt and _doubled(syl, nxt):
            coda = coda[:-1]

        body = "".join([*onset, syl.nucleus.ipa, *coda])
        out.append(f"ˈ{body}" if i == word.stress and len(syllables) > 1 else body)
    return ".".join(out)


def _doubled(a: Syllable, b: Syllable) -> bool:
    return bool(a.coda and b.onset and a.coda[-1].text == b.onset[0].text)
