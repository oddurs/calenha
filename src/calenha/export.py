"""The data contract between the language and the website.

``export`` compiles everything in ``lang/`` (and the prose in ``docs/`` and
``context/``) into one JSON document. The Svelte site reads only this file, so it
never needs to know the language's rules — only what they produced. The shape is
mirrored in ``web/src/lib/language/types.ts``; change both together.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

from . import __version__, mdown
from .generate import generate
from .language import Entry, Language
from .render import POS_LABEL, collate, explain_parts, short_gloss, sorted_entries, stats
from .sound_change import evolve
from .validate import words_of

SCHEMA = 1

# documents rendered from Markdown: key → (source, lede)
DOCS = {
    "grammar": (
        "docs/grammar.md",
        "Invitations, tide-time, the breath and the bow: how the calm speech works.",
    ),
    "sounds": ("docs/phonology.md", "How Calenha sounds, and how it is written."),
    "world": ("context/world.md", "Solmara, and the people who speak Calenha there."),
    "principles": ("context/principles.md", "The rules behind the rules. What must never be lost."),
}

# code spans in the documents that name another page of the site (relative links)
DOC_LINKS = {
    "docs/grammar.md": "grammar",
    "docs/phonology.md": "sounds",
    "context/world.md": "world",
    "context/principles.md": "principles",
    "lang/roots.toml": "roots",
    "lang/affixes.toml": "roots#endings",
    "lang/sound-changes.toml": "history",
}

TOPICS = ["greetings", "the hours", "the heart", "land and sea", "sayings"]

_EMPHASIS = re.compile(r"<(strong|em)>(.*?)</\1>", re.S)


def tag_calenha(html: str, language: Language) -> str:
    """Mark emphasised runs that are wholly Calenha with ``lang="x-calenha"``.

    The documents set Calenha examples in bold or italics. Tagging them lets the site
    give them Calenha's voice, while English emphasis is left as it is.
    """

    def tag(m: re.Match[str]) -> str:
        words = words_of(re.sub(r"<[^>]+>", "", m.group(2)).lstrip("*-"))
        if words and all(language.lookup(w) or w in language.roots for w in words):
            return f'<{m.group(1)} lang="x-calenha">{m.group(2)}</{m.group(1)}>'
        return m.group(0)

    return _EMPHASIS.sub(tag, html)


def slugs(entries: list[Entry]) -> dict[int, str]:
    """A readable, unique address for every entry.

    The spelling without accents; on a collision, a nasal spelled out (nã → nan);
    failing that, the gloss appended (salva-thank-you).
    """
    taken: set[str] = set()
    out: dict[int, str] = {}
    for entry in entries:
        plain = collate(entry.word)
        nasal = collate(entry.word.replace("ã", "an").replace("õ", "on"))
        glossed = f"{plain}-{collate(short_gloss(entry)).replace(' ', '-')}"
        slug = next(s for s in (plain, nasal, glossed) if s not in taken)
        taken.add(slug)
        out[id(entry)] = slug
    return out


def export(language: Language, root: Path, *, built: str | None = None) -> dict[str, Any]:
    entries = sorted_entries(language)
    slug = slugs(entries)
    phonology = language.phonology
    change_index = {c.name: i for i, c in enumerate(language.sound_changes, start=1)}

    def slug_of(word: str) -> str | None:
        found = language.lookup(word)
        return slug[id(found[0])] if found else None

    def word_shape(text: str) -> dict[str, Any]:
        word = phonology.syllabify(text)
        return {
            "syllables": [s.text for s in word.syllables],
            "stress": word.stress,
            "ipa": word.ipa(),
        }

    def part(entry: Entry, form: str, meaning: str) -> dict[str, Any]:
        if form in language.roots:
            kind, target = "root", collate(form)
        elif form.startswith("-") or form.endswith("-"):
            kind, target = "affix", None
        else:
            kind, target = "word", slug_of(form)
        return {"form": form, "meaning": meaning, "kind": kind, "target": target}

    out_entries = []
    for entry in entries:
        roots = language.ancestry(entry)
        family = {slug[id(e)] for r in roots for e in language.children(r) if e.word != entry.word}
        history = []
        if entry.old:
            for step in evolve(entry.old, language).steps:
                history.append(
                    {
                        "form": step.after,
                        "change": step.change.name,
                        "index": change_index[step.change.name],
                    }
                )
        out_entries.append(
            {
                "slug": slug[id(entry)],
                "word": entry.word,
                "gloss": entry.gloss,
                "short": short_gloss(entry),
                "pos": entry.pos,
                "label": POS_LABEL[entry.pos],
                "domain": entry.domain,
                "sense": entry.sense,
                **word_shape(entry.word),
                "parts": [part(entry, f, m) for f, m in explain_parts(entry, language)],
                "old": entry.old,
                "history": history,
                "family": sorted(family, key=collate),
                "phrases": [
                    i for i, p in enumerate(language.phrases) if entry.word in words_of(p.text)
                ],
                "texts": [
                    t.slug
                    for t in language.texts
                    if any(entry.word in words_of(line.text) for line in t.lines)
                ],
            }
        )

    roots = [
        {
            "root": r.root,
            "slug": collate(r.root),
            "meaning": r.meaning,
            "kin": r.kin,
            "children": [slug[id(e)] for e in sorted_entries_of(language.children(r.root))],
        }
        for r in language.roots.values()
    ]

    affixes = [
        {
            "form": a.form,
            "meaning": a.meaning,
            "makes": a.makes,
            "examples": [
                slug[id(e)] for e in entries if a.form in e.parts and a.makes in (e.pos, "link")
            ][:4],
        }
        for a in language.affixes
    ]

    shaped: dict[str, list[str]] = {c.name: [] for c in language.sound_changes}
    for entry in entries:
        if entry.old:
            for step in evolve(entry.old, language).steps:
                shaped[step.change.name].append(slug[id(entry)])
    changes = []
    for i, c in enumerate(language.sound_changes, start=1):
        pairs = c.pairs or {c.find: c.replace}
        changes.append(
            {
                "index": i,
                "name": c.name,
                "rule": [[a, b] for a, b in pairs.items()],
                "when": c.when,
                "environment": environment(c.when),
                "note": tag_calenha(mdown.inline(c.note), language),
                "shaped": shaped[c.name],
            }
        )

    def candidates(kind: str, seed: int, n: int) -> list[dict[str, Any]]:
        return [
            {"text": c.word.text, **word_shape(c.word.text), "echoes": list(c.echoes)}
            for c in generate(language, n=n, seed=seed, syllables=(2, 3), kind=kind)
        ]

    seed = len(language.entries)  # the unspoken change as the lexicon grows

    docs = {}
    for key, (source, lede) in DOCS.items():
        doc = mdown.render((root / source).read_text(encoding="utf-8"), link=DOC_LINKS.get)
        docs[key] = {"title": doc.title, "lede": lede, "html": tag_calenha(doc.html, language)}

    return {
        "schema": SCHEMA,
        "meta": {
            "version": __version__,
            "built": built or date.today().isoformat(),
            "counts": stats(language),
        },
        "domains": [{"name": d, "intro": intro} for d, intro in language.domains.items()],
        "topics": TOPICS,
        "entries": out_entries,
        "roots": roots,
        "affixes": affixes,
        "phrases": [
            {
                "text": p.text,
                "literal": p.literal,
                "translation": p.translation,
                "topic": p.topic,
                "featured": p.featured,
            }
            for p in language.phrases
        ],
        "texts": [
            {
                "slug": t.slug,
                "title": t.title,
                "english": t.english,
                "kind": t.kind,
                "note": tag_calenha(mdown.inline(t.note), language),
                "lines": [{"text": ln.text, "translation": ln.translation} for ln in t.lines],
            }
            for t in language.texts
        ],
        "changes": changes,
        "unspoken": {
            "things": candidates("noun", seed, 24),
            "invitations": candidates("verb", seed + 1, 12),
        },
        "docs": docs,
    }


def sorted_entries_of(entries: list[Entry]) -> list[Entry]:
    return sorted(entries, key=lambda e: (collate(e.word), e.word))


def environment(when: str) -> str:
    """``l_`` → ``after l``; ``_V`` → ``before a vowel``; ``_#`` → ``at the end of a word``."""
    if not when:
        return ""
    left, _, right = when.partition("_")

    def name(part: str) -> str:
        return {"V": "a vowel", "C": "a consonant"}.get(part, part)

    phrases = []
    left = left.replace("#", "")
    if left:
        phrases.append(f"after {name(left)}")
    if right == "#":
        phrases.append("at the end of a word")
    elif right.endswith("#"):
        phrases.append(f"before {name(right[:-1])}, at the end")
    elif right:
        phrases.append(f"before {name(right)}")
    return ", ".join(phrases)
