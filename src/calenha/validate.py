"""Holding the language to its own rules.

``check`` returns a list of :class:`Issue`. Errors mean the data contradicts the
rules and must be fixed; warnings mean something is unfinished or lonely.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .language import PARTS_OF_SPEECH, Language
from .morphology import join
from .phonology import BREATH, PhonologyError, normalize

ERROR = "error"
WARNING = "warning"


@dataclass(frozen=True)
class Issue:
    level: str
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.level}: {self.where}: {self.message}"


def check(language: Language) -> list[Issue]:
    issues: list[Issue] = []
    issues += _check_roots(language)
    issues += _check_entries(language)
    issues += _check_phrases(language)
    issues += _check_sound_changes(language)
    return issues


def errors(issues: list[Issue]) -> list[Issue]:
    return [i for i in issues if i.level == ERROR]


# -- roots ---------------------------------------------------------------------


def _check_roots(language: Language) -> list[Issue]:
    issues = []
    used = {root for entry in language.entries for root in language.ancestry(entry)}
    for root in language.roots.values():
        where = f"root {root.root}"
        try:
            language.phonology.tokenize(root.root)
        except PhonologyError as e:
            issues.append(Issue(ERROR, where, e.reason))
        if root.root not in used:
            issues.append(Issue(WARNING, where, "no word grows from this root yet"))
    return issues


# -- entries -------------------------------------------------------------------


def _check_entries(language: Language) -> list[Issue]:
    issues = []
    phonology = language.phonology
    seen = Counter((e.word, e.pos) for e in language.entries)

    for entry in language.entries:
        where = f"{entry.domain}: {entry.word}"

        def err(message: str, where: str = where) -> None:
            issues.append(Issue(ERROR, where, message))

        for problem in phonology.problems(entry.word):
            err(problem)

        if seen[(entry.word, entry.pos)] > 1:
            err(f"defined more than once as a {entry.pos}")

        if entry.pos not in PARTS_OF_SPEECH:
            err(f"unknown part of speech {entry.pos!r}")
        elif entry.pos == "verb" and not entry.word.endswith("u"):
            err("every verb ends in -u — the invitation")
        elif entry.pos in ("noun", "adjective", "name") and entry.word.endswith("u"):
            err("only verbs may end in -u")

        if entry.gloss != entry.gloss.strip() or entry.gloss.endswith("."):
            err("a gloss has no full stop and no stray spaces")
        if entry.gloss[:1].isupper() and entry.gloss.split()[0] not in ("I",):
            err("a gloss is lowercase")

        if entry.parts:
            for part in entry.parts:
                if not _is_morpheme(language, part):
                    err(f"{part!r} is not a root, an affix or a word")
            built = join(entry.parts, phonology)
            if built != entry.word:
                err(f"{' + '.join(entry.parts)} gives {built!r}, not {entry.word!r}")

    return issues


def _is_morpheme(language: Language, part: str) -> bool:
    if part.startswith("-") or part.endswith("-"):
        return bool(language.affix(part))
    return part in language.roots or bool(language.lookup(part))


# -- phrases -------------------------------------------------------------------

_PUNCTUATION = re.compile(r"[.,;:!?\"'—–]")


def words_of(text: str) -> list[str]:
    """The words of a line, stripped of punctuation, capitals and breath marks."""
    text = _PUNCTUATION.sub(" ", normalize(text))
    return [w.replace(BREATH, "") for w in text.split() if w.replace(BREATH, "")]


def _check_phrases(language: Language) -> list[Issue]:
    issues = []
    for phrase in language.phrases:
        for word in words_of(phrase.text):
            if not language.lookup(word):
                issues.append(Issue(ERROR, f"phrase {phrase.text!r}", f"{word!r} is not a word"))
    return issues


# -- old forms -----------------------------------------------------------------


def _check_sound_changes(language: Language) -> list[Issue]:
    if not language.sound_changes:
        return []
    from .sound_change import evolve

    issues = []
    for entry in language.entries:
        if entry.old is None:
            continue
        result = evolve(entry.old, language).word
        if result != entry.word:
            issues.append(
                Issue(
                    ERROR,
                    f"{entry.domain}: {entry.word}",
                    f"old form *{entry.old} becomes {result!r}, not {entry.word!r}",
                )
            )
    return issues
