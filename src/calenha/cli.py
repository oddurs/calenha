"""``calenha`` — the command line.

calenha check            hold the language to its rules
calenha show WORD…       everything about a word
calenha read "LINE"      gloss a line of Calenha word by word
calenha gen              coin new words, ranked by euphony
calenha evolve OLD…      run an old form through the sound changes
calenha build            write the dictionary to dist/
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

from . import __version__
from .export import export
from .generate import euphony, generate
from .language import Language
from .paths import lang_dir
from .phonology import BREATH, PhonologyError, normalize
from .render import POS_LABEL, explain_parts, markdown, stats
from .sound_change import evolve
from .validate import ERROR, check, words_of

DATA = Path("web/src/lib/data/language.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calenha", description="Calenha — the calm speech. Tools for the language."
    )
    parser.add_argument("--lang", type=Path, help="path to the lang/ directory")
    parser.add_argument("--version", action="version", version=f"calenha {__version__}")
    sub = parser.add_subparsers(dest="command", required=True, metavar="command")

    p = sub.add_parser("check", help="validate the whole language")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")

    p = sub.add_parser("show", help="syllables, stress, pronunciation and history of words")
    p.add_argument("words", nargs="+")

    p = sub.add_parser("read", help="gloss a line of Calenha word by word")
    p.add_argument("line")

    p = sub.add_parser("gen", help="coin candidate words, most beautiful first")
    p.add_argument("-n", type=int, default=12, help="how many (default 12)")
    p.add_argument("--syllables", default="2-3", help="a count or range, e.g. 3 or 2-4")
    p.add_argument("--verb", action="store_true", help="coin verbs (ending in -u)")
    p.add_argument("--seed", type=int, help="repeatable results")

    p = sub.add_parser("evolve", help="run old forms through the sound changes")
    p.add_argument("forms", nargs="+")

    p = sub.add_parser("export", help="write the language as JSON for the website")
    p.add_argument("--out", type=Path, help=f"default: {DATA}")

    p = sub.add_parser("build", help="export, and write dist/dictionary.md")
    p.add_argument("--out", type=Path, default=Path("dist"))

    args = parser.parse_args(argv)
    lang = (args.lang or lang_dir()).resolve()
    language = Language.load(lang)
    args.root = lang.parent
    return COMMANDS[args.command](language, args)


# -- commands -------------------------------------------------------------------


def cmd_check(language: Language, args: argparse.Namespace) -> int:
    issues = check(language)
    for issue in issues:
        print(issue)
    counts = stats(language)
    summary = ", ".join(f"{n} {label}" for label, n in counts.items())
    failed = [i for i in issues if i.level == ERROR or args.strict]
    if failed:
        print(f"\n{len(failed)} to mend · {summary}")
        return 1
    print(f"calenha is well · {summary}")
    return 0


def cmd_show(language: Language, args: argparse.Namespace) -> int:
    status = 0
    for i, raw in enumerate(args.words):
        if i:
            print()
        text = normalize(raw).replace(BREATH, "")
        try:
            word = language.phonology.syllabify(text)
        except PhonologyError as e:
            print(f"{raw}: {e.reason}")
            status = 1
            continue

        entries = language.lookup(text)
        print(f"{word.text}   {word.hyphenated()}   /{word.ipa()}/")
        if not entries:
            problems = language.phonology.problems(text)
            print("  " + ("; ".join(problems) if problems else "not a word yet — but it could be"))
            score = euphony(word, language.phonology)
            print(f"  euphony {score:.2f}")
        for entry in entries:
            print(f"  {POS_LABEL[entry.pos]} — {entry.gloss}")
            if entry.sense:
                print(_wrap(entry.sense, "  “", "”"))
            if entry.parts:
                parts = " + ".join(f"{p} ({m})" for p, m in explain_parts(entry, language))
                print(_wrap(parts, "  from "))
            if entry.old:
                print(f"  older *{entry.old}")
        if text in language.roots:
            root = language.roots[text]
            children = [e.word for e in language.children(text)]
            print(f"  root — {root.meaning}")
            if children:
                print(_wrap(", ".join(children), "  grows into "))
    return status


def cmd_read(language: Language, args: argparse.Namespace) -> int:
    print(args.line)
    unknown = 0
    for word in words_of(args.line):
        entries = language.lookup(word)
        if entries:
            print(f"  {word:<12} {entries[0].gloss}")
        else:
            print(f"  {word:<12} ?")
            unknown += 1
    return 1 if unknown else 0


def cmd_gen(language: Language, args: argparse.Namespace) -> int:
    low, _, high = args.syllables.partition("-")
    span = (int(low), int(high or low))
    kind = "verb" if args.verb else "noun"
    for c in generate(language, n=args.n, syllables=span, kind=kind, seed=args.seed):
        echo = f"   echoes {', '.join(c.echoes)}" if c.echoes else ""
        print(f"{c.score:.2f}  {c.word.text:<14} {c.word.hyphenated():<16} /{c.word.ipa()}/{echo}")
    return 0


def cmd_evolve(language: Language, args: argparse.Namespace) -> int:
    for i, form in enumerate(args.forms):
        if i:
            print()
        result = evolve(form, language)
        print(f"*{result.old}")
        for step in result.steps:
            print(f"  → {step.after:<14} {step.change.name}")
        print(f"= {result.word}" + ("" if result.steps else "   (unchanged)"))
    return 0


def cmd_export(language: Language, args: argparse.Namespace) -> int:
    if issues := [i for i in check(language) if i.level == ERROR]:
        for issue in issues:
            print(issue)
        print("\nnot exporting: run `calenha check` and mend these first")
        return 1
    out = args.out or args.root / DATA
    out.parent.mkdir(parents=True, exist_ok=True)
    data = export(language, args.root)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} — {data['meta']['counts']['words']} words")
    return 0


def cmd_build(language: Language, args: argparse.Namespace) -> int:
    dist = args.out
    args.out = None
    if status := cmd_export(language, args):
        return status
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "dictionary.md").write_text(markdown(language), encoding="utf-8")
    print(f"wrote {dist / 'dictionary.md'} — the website builds from web/ (npm run build)")
    return 0


COMMANDS = {
    "check": cmd_check,
    "show": cmd_show,
    "read": cmd_read,
    "gen": cmd_gen,
    "evolve": cmd_evolve,
    "export": cmd_export,
    "build": cmd_build,
}


def _wrap(text: str, first: str, last: str = "") -> str:
    return textwrap.fill(
        text + last, width=78, initial_indent=first, subsequent_indent=" " * len(first)
    )


if __name__ == "__main__":
    sys.exit(main())
