"""The whole language, loaded from ``lang/`` into plain, immutable records."""

from __future__ import annotations

import tomllib
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from .phonology import Phonology, normalize

PARTS_OF_SPEECH = ("noun", "verb", "adjective", "name", "particle", "pronoun")


@dataclass(frozen=True)
class Root:
    root: str
    meaning: str
    kin: str | None = None


@dataclass(frozen=True)
class Affix:
    form: str
    meaning: str
    makes: str

    @property
    def bare(self) -> str:
        return self.form.strip("-")


@dataclass(frozen=True)
class Entry:
    word: str
    gloss: str
    pos: str
    domain: str
    parts: tuple[str, ...] = ()
    old: str | None = None
    sense: str | None = None

    @property
    def is_derived(self) -> bool:
        return bool(self.parts)


@dataclass(frozen=True)
class Phrase:
    text: str
    literal: str
    translation: str
    featured: bool = False


@dataclass(frozen=True)
class SoundChange:
    name: str
    find: str = ""
    replace: str = ""
    pairs: dict[str, str] = field(default_factory=dict)
    when: str = ""
    note: str = ""


@dataclass
class Language:
    phonology: Phonology
    roots: dict[str, Root] = field(default_factory=dict)
    affixes: list[Affix] = field(default_factory=list)
    entries: list[Entry] = field(default_factory=list)
    phrases: list[Phrase] = field(default_factory=list)
    sound_changes: list[SoundChange] = field(default_factory=list)
    domains: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, lang: Path) -> Language:
        language = cls(Phonology.load(lang / "phonology.toml"))

        for spec in _read(lang / "roots.toml").get("root", []):
            root = Root(normalize(spec["root"]), spec["meaning"], spec.get("kin"))
            language.roots[root.root] = root

        for spec in _read(lang / "affixes.toml").get("affix", []):
            language.affixes.append(Affix(normalize(spec["form"]), spec["meaning"], spec["makes"]))

        for path in sorted((lang / "lexicon").glob("*.toml")):
            language.domains[path.stem] = _intro(path)
            for spec in _read(path).get("word", []):
                language.entries.append(
                    Entry(
                        word=normalize(spec["word"]),
                        gloss=spec["gloss"],
                        pos=spec["pos"],
                        domain=path.stem,
                        parts=tuple(normalize(p) for p in spec.get("from", ())),
                        old=normalize(spec["old"]) if "old" in spec else None,
                        sense=spec.get("sense"),
                    )
                )

        phrases = lang / "phrases.toml"
        if phrases.exists():
            language.phrases = [Phrase(**p) for p in _read(phrases).get("phrase", [])]

        changes = lang / "sound-changes.toml"
        if changes.exists():
            language.sound_changes = [SoundChange(**c) for c in _read(changes).get("change", [])]

        return language

    # -- looking things up ---------------------------------------------------------

    def lookup(self, word: str) -> list[Entry]:
        return self._by_word.get(normalize(word), [])

    def children(self, root: str) -> list[Entry]:
        """Every word that grows from a root (directly, or through another word)."""
        found = []
        for entry in self.entries:
            if root in self.ancestry(entry):
                found.append(entry)
        return found

    def ancestry(self, entry: Entry, _seen: frozenset[str] = frozenset()) -> set[str]:
        """All roots a word descends from."""
        roots: set[str] = set()
        if not entry.parts and entry.word in self.roots:
            roots.add(entry.word)
        for part in entry.parts:
            if part in self.roots:
                roots.add(part)
            elif part not in _seen:
                for parent in self.lookup(part):
                    roots |= self.ancestry(parent, _seen | {entry.word})
        return roots

    def affix(self, form: str) -> list[Affix]:
        return [a for a in self.affixes if a.form == normalize(form)]

    @cached_property
    def _by_word(self) -> dict[str, list[Entry]]:
        index: dict[str, list[Entry]] = defaultdict(list)
        for entry in self.entries:
            index[entry.word].append(entry)
        return index


def _read(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def _intro(path: Path) -> str:
    """The first comment line of a lexicon file — its one-line description."""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            return line.lstrip("# ").strip()
        if line.strip():
            break
    return ""
