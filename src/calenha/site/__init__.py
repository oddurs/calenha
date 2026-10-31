"""The website: the dictionary, a page for every word, and the language's documents.

Everything is generated from ``lang/`` and the Markdown in ``docs/`` and ``context/``.
The output is plain static HTML with one stylesheet — no build tools, no runtime.
"""

from __future__ import annotations

import html
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from importlib import resources
from pathlib import Path

from ..generate import generate
from ..language import Entry, Language
from ..render import (
    POS_LABEL,
    collate,
    explain_parts,
    line_html,
    sorted_entries,
    stats,
    stressed_html,
)
from ..sound_change import evolve
from ..validate import words_of
from . import mdown

REPO = "https://github.com/oddurs/calenha"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400"
    "&display=swap"
)

NAV = [
    ("words", "words.html"),
    ("roots", "roots.html"),
    ("grammar", "grammar.html"),
    ("sounds", "sounds.html"),
    ("history", "history.html"),
    ("world", "world.html"),
    ("unspoken", "unspoken.html"),
]

# documents rendered from Markdown: page → (source, lede)
DOCS = {
    "grammar.html": (
        "docs/grammar.md",
        "Very little grammar, and every piece of it means something.",
    ),
    "sounds.html": ("docs/phonology.md", "How Calenha sounds, and how it is written."),
    "world.html": ("context/world.md", "Solmara, and the people who speak Calenha there."),
    "principles.html": (
        "context/principles.md",
        "The rules behind the rules. What must never be lost.",
    ),
}

# code spans in the documents that name another page of the site
DOC_LINKS = {
    "docs/grammar.md": "grammar.html",
    "docs/phonology.md": "sounds.html",
    "context/world.md": "world.html",
    "context/principles.md": "principles.html",
    "lang/roots.toml": "roots.html",
    "lang/affixes.toml": "roots.html#endings",
    "lang/sound-changes.toml": "history.html",
}

FIVE_THINGS = [
    (
        "every verb is an invitation",
        "nã velu · calu.",
        "Verbs end in -u, and there is no way to command. This line means "
        "“there’s no need to wander; rest.”",
    ),
    (
        "time is a tide",
        "vaza nevoã · chea solouro.",
        "Vaza (ebb) marks what has passed, chea (flood) what is coming. "
        "“The fog has gone out; the golden hour is coming in.”",
    ),
    (
        "a space can be a silence",
        "aswen tu velu · solenha.",
        "The breath mark is a pause that closes a condition, the way a block ends. "
        "“If you wander, there will be light through the leaves.”",
    ),
    (
        "capitals are a bow",
        "lë Miraluma miru.",
        "Everything is lowercase, so a capital is reverence. “The redwood remembers.”",
    ),
    (
        "words grow from roots",
        "thalírë · altavel",
        "Thal (flow) and -írë (the ever-) make the river. Alt (high) and vel (wander) "
        "make the condor, the high wanderer.",
    ),
]


@dataclass
class Site:
    language: Language
    root: Path
    built: str = field(default_factory=lambda: date.today().isoformat())

    def __post_init__(self) -> None:
        self.entries = sorted_entries(self.language)
        self.slugs: dict[int, str] = {}
        taken: dict[str, int] = {}
        for entry in self.entries:
            slug = collate(entry.word)
            if slug in taken:
                slug = f"{slug}-{entry.pos}"
            taken[slug] = 1
            self.slugs[id(entry)] = slug
        self.change_index = {c.name: i + 1 for i, c in enumerate(self.language.sound_changes)}

    # -- addresses --------------------------------------------------------------

    def word_path(self, entry: Entry) -> str:
        return f"word/{self.slugs[id(entry)]}.html"

    def word_href(self, depth: int) -> Callable[[str], str | None]:
        prefix = "../" * depth

        def href(word: str) -> str | None:
            found = self.language.lookup(word)
            return prefix + self.word_path(found[0]) if found else None

        return href

    # -- the frame ---------------------------------------------------------------

    def layout(
        self,
        title: str,
        body: str,
        *,
        depth: int = 0,
        current: str = "",
        description: str = "",
        fragment: bool = False,
        script: str = "",
    ) -> str:
        pre = "../" * depth
        nav = "".join(
            f'<a href="{pre}{href}"'
            + (' aria-current="page"' if href == current else "")
            + f">{label}</a>"
            for label, href in NAV
        )
        head = (
            f"<title>{html.escape(title)}</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            + (
                f'<meta name="description" content="{html.escape(description)}">\n'
                if description
                else ""
            )
            + '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="{FONTS}">\n'
            f'<link rel="stylesheet" href="{pre}site.css">\n'
        )
        page = f"""<header class="top"><div class="wrap">
<a class="home" href="{pre}index.html">calenha</a>
<nav class="nav" aria-label="Sections">{nav}</nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">
<a href="{pre}principles.html">principles</a>
<a href="{REPO}">source</a>
<span>built {self.built} from the language’s own data</span>
</div></footer>
{script}"""
        if fragment:
            return head + page
        return (
            '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, '
            'viewport-fit=cover">\n'
            f"{head}</head>\n<body>\n{page}\n</body>\n</html>\n"
        )

    def heading(self, title: str, lede: str = "") -> str:
        lede_html = f'<p class="lede">{html.escape(lede)}</p>' if lede else ""
        return f'<div class="head"><h1>{html.escape(title)}</h1>{lede_html}</div>'

    # -- pages --------------------------------------------------------------------

    def pages(self, *, fragment_home: bool = False) -> dict[str, str]:
        out = {
            "index.html": self.home(fragment=fragment_home),
            "words.html": self.words(),
            "roots.html": self.roots(),
            "history.html": self.history(),
            "unspoken.html": self.unspoken(),
        }
        for path, (source, lede) in DOCS.items():
            out[path] = self.document(path, source, lede)
        for i, entry in enumerate(self.entries):
            before = self.entries[i - 1] if i else None
            after = self.entries[i + 1] if i + 1 < len(self.entries) else None
            out[self.word_path(entry)] = self.word(entry, before, after)
        return out

    def home(self, *, fragment: bool = False) -> str:
        language = self.language
        counts = stats(language)
        featured = next((p for p in language.phrases if p.featured), language.phrases[0])
        link = self.word_href(0)

        things = "".join(
            f"<li><h3>{html.escape(title)}</h3>"
            f'<p class="ex" lang="x-calenha">{line_html(example, language, link)}</p>'
            f"<p>{html.escape(text)}</p></li>"
            for title, example, text in FIVE_THINGS
        )
        ways = [
            (
                "words",
                "words.html",
                f"all {counts['words']} words, searchable, in Calenha or English",
            ),
            ("roots", "roots.html", f"the {counts['roots']} roots and the endings words grow from"),
            ("grammar", "grammar.html", "invitation, tide-time, the breath, the bow"),
            ("sounds", "sounds.html", "vowels, consonants, syllables and stress"),
            ("history", "history.html", "how Old Calenha softened into the modern tongue"),
            ("world", "world.html", "Solmara and the Calenhi"),
            ("unspoken", "unspoken.html", "words the ear has found that mean nothing yet"),
        ]
        ways_html = "".join(
            f'<li><a href="{href}"><b>{label}</b><span>{html.escape(text)}</span></a></li>'
            for label, href, text in ways
        )
        body = f"""<header class="hero">
<p class="line" lang="x-calenha">{line_html(featured.text, language)}</p>
<p class="tr">{html.escape(featured.translation)}</p>
<div class="intro">
<p>Calenha is the calm speech of the Calenhi of Solmara, a California one step to the side
of ours, where nothing was ever hurried. It sounds like Portuguese with a touch of English,
and it takes its silences seriously.</p>
<p>Gold marks the syllable that carries the stress. Tap a word in any example to
visit its own page.</p>
</div>
</header>
<section class="part" aria-labelledby="h-five">
<h2 id="h-five">five things to know</h2>
<ul class="things">{things}</ul>
</section>
<section class="part" aria-labelledby="h-begin">
<h2 id="h-begin">where to begin</h2>
<ul class="ways">{ways_html}</ul>
</section>
<section class="part" aria-labelledby="h-use">
<h2 id="h-use">in use</h2>
<ul class="phrases">{self.phrase_items(language.phrases, 0, skip=featured)}</ul>
</section>"""
        return self.layout(
            "Calenha",
            body,
            description="Calenha, the calm speech: a constructed language for a mythical California.",
            fragment=fragment,
        )

    def phrase_items(self, phrases, depth: int, skip=None) -> str:
        link = self.word_href(depth)
        return "".join(
            f'<li><p class="cal" lang="x-calenha">{line_html(p.text, self.language, link)}</p>'
            f'<p class="lit">{html.escape(p.literal)}</p>'
            f'<p class="tr">{html.escape(p.translation)}</p></li>'
            for p in phrases
            if p is not skip
        )

    def parts_inline(self, entry: Entry, depth: int) -> str:
        pre = "../" * depth
        bits = []
        for part, meaning in explain_parts(entry, self.language):
            target = self.part_href(part, pre)
            name = html.escape(part)
            shown = f'<a href="{target}">{name}</a>' if target else f"<span>{name}</span>"
            bits.append(shown + (f" <i>{html.escape(meaning)}</i>" if meaning else ""))
        return " + ".join(bits)

    def part_href(self, part: str, pre: str) -> str | None:
        if part in self.language.roots:
            return f"{pre}roots.html#r-{collate(part)}"
        if part.startswith("-") or part.endswith("-"):
            return f"{pre}roots.html#endings"
        found = self.language.lookup(part)
        return pre + self.word_path(found[0]) if found else None

    def words(self) -> str:
        language = self.language
        counts = stats(language)
        groups: list[tuple[str, list[str]]] = []
        for entry in self.entries:
            initial = collate(entry.word)[0]
            if not groups or groups[-1][0] != initial:
                groups.append((initial, []))
            groups[-1][1].append(self.entry_html(entry))
        dictionary = "\n".join(
            f'<section class="letter"><h3>{letter}</h3>{"".join(items)}</section>'
            for letter, items in groups
        )
        chips = "".join(
            f'<button type="button" class="chip" id="d-{d}" data-domain="{d}" '
            f'aria-pressed="false" title="{html.escape(intro)}">{d}</button>'
            for d, intro in language.domains.items()
        )
        body = f"""{self.heading("words", "From the sea inward, the way the fog travels.")}
<div class="find">
<label for="q">Find a word in Calenha or English</label>
<input id="q" type="search" placeholder="river, mirão, light…" autocomplete="off" spellcheck="false">
<div class="chips" role="group" aria-label="Filter by domain">
<button type="button" class="chip" id="d-all" data-domain="" aria-pressed="true">all</button>{chips}
</div>
<p class="count" id="count" aria-live="polite">{counts["words"]} words</p>
</div>
<p id="empty" hidden>No word for that yet. Try it in English or in Calenha, or see the
<a href="unspoken.html">unspoken words</a> waiting for a meaning.</p>
<div id="dictionary">{dictionary}</div>"""
        return self.layout(
            "words — calenha",
            body,
            current="words.html",
            description=f"The Calenha dictionary: {counts['words']} words.",
            script=FILTER_SCRIPT,
        )

    def entry_html(self, entry: Entry) -> str:
        word = self.language.phonology.syllabify(entry.word)
        search = " ".join(
            filter(None, [entry.word, collate(entry.word), entry.gloss, entry.sense or ""])
        ).lower()
        bits = [
            f'<article class="entry" data-domain="{entry.domain}" '
            f'data-search="{html.escape(search)}">',
            f'<h4 class="hw" lang="x-calenha"><a href="{self.word_path(entry)}">'
            f"{stressed_html(word)}</a></h4>",
            '<div class="body">',
            f'<p class="gloss">{html.escape(entry.gloss)}'
            f' <span class="pos">{POS_LABEL[entry.pos]}</span></p>',
            f'<p class="ipa">/{html.escape(word.ipa())}/</p>',
        ]
        if entry.sense:
            bits.append(f'<p class="sense">{html.escape(entry.sense)}</p>')
        ety = []
        if entry.parts:
            ety.append(self.parts_inline(entry, 0))
        if entry.old:
            ety.append(f'from older <span lang="x-calenha">*{html.escape(entry.old)}</span>')
        if ety:
            bits.append(f'<p class="ety">{"; ".join(ety)}</p>')
        bits += ["</div>", "</article>"]
        return "\n".join(bits)

    def word(self, entry: Entry, before: Entry | None, after: Entry | None) -> str:
        language = self.language
        word = language.phonology.syllabify(entry.word)
        facts: list[tuple[str, str]] = []

        if entry.parts:
            parts = []
            for part, meaning in explain_parts(entry, language):
                target = self.part_href(part, "../")
                name = html.escape(part)
                shown = (
                    f'<a href="{target}">{name}</a>' if target else f'<span class="f">{name}</span>'
                )
                parts.append(
                    f'<span class="part-m" lang="x-calenha">{shown}<i>{html.escape(meaning)}</i></span>'
                )
            facts.append(
                ("made from", f'<p class="parts">{"<span class=plus>+</span>".join(parts)}</p>')
            )

        if entry.old:
            result = evolve(entry.old, language)
            chain = [f'<span class="old" lang="x-calenha">*{html.escape(result.old)}</span>']
            for step in result.steps:
                n = self.change_index[step.change.name]
                chain.append(
                    '<span class="to">→</span>'
                    f'<span lang="x-calenha">{html.escape(step.after)}'
                    f'<small><a href="../history.html#c-{n}">{html.escape(step.change.name)}</a></small></span>'
                )
            facts.append(("history", f'<p class="chain">{"".join(chain)}</p>'))

        roots = language.ancestry(entry)
        family = sorted(
            {
                e.word: e for root in roots for e in language.children(root) if e.word != entry.word
            }.values(),
            key=lambda e: collate(e.word),
        )
        if family:
            items = "".join(
                f'<li><a href="{self.slugs[id(e)]}.html" lang="x-calenha">{html.escape(e.word)}</a> '
                f"<i>{html.escape(e.gloss)}</i></li>"
                for e in family
            )
            facts.append(("family", f'<ul class="kin">{items}</ul>'))

        used = [p for p in language.phrases if entry.word in words_of(p.text)]
        if used:
            facts.append(("in use", f'<ul class="phrases">{self.phrase_items(used, 1)}</ul>'))

        facts_html = "".join(
            f'<div class="fact"><h2>{t}</h2><div>{b}</div></div>' for t, b in facts
        )
        sense = f'<p class="word-sense">{html.escape(entry.sense)}</p>' if entry.sense else ""
        pager = '<nav class="pager" aria-label="Neighbouring words">'
        pager += (
            f'<a href="{self.slugs[id(before)]}.html" rel="prev">← {html.escape(before.word)}</a>'
            if before
            else "<span></span>"
        )
        pager += (
            f'<a href="{self.slugs[id(after)]}.html" rel="next">{html.escape(after.word)} →</a>'
            if after
            else "<span></span>"
        )
        pager += "</nav>"

        body = f"""<article>
<header class="word-head">
<h1 lang="x-calenha">{stressed_html(word)}</h1>
<p class="say"><span class="syl">{html.escape(word.hyphenated())}</span><span class="ipa">/{html.escape(word.ipa())}/</span></p>
<p class="meaning">{html.escape(entry.gloss)} <span class="pos">{POS_LABEL[entry.pos]}</span></p>
{sense}
</header>
<div class="facts">{facts_html}</div>
{pager}
</article>"""
        return self.layout(
            f"{entry.word} — calenha",
            body,
            depth=1,
            current="",
            description=f"{entry.word}: {entry.gloss}. A word of Calenha.",
        )

    def roots(self) -> str:
        language = self.language
        items = []
        for root in language.roots.values():
            children = language.children(root.root)
            kids = "".join(
                f'<a href="{self.word_path(e)}" lang="x-calenha">{html.escape(e.word)}</a>'
                for e in children
            )
            kin = f'<p class="k">{html.escape(root.kin)}</p>' if root.kin else ""
            items.append(
                f'<li id="r-{collate(root.root)}"><p class="r" lang="x-calenha">{html.escape(root.root)}</p>'
                f'<div><p class="m">{html.escape(root.meaning)}</p>{kin}<p class="c">{kids}</p></div></li>'
            )

        endings = []
        for affix in language.affixes:
            users = [
                e
                for e in self.entries
                if affix.form in e.parts and (affix.makes in (e.pos, "link"))
            ]
            examples = ", ".join(
                f'<a href="{self.word_path(e)}" lang="x-calenha">{html.escape(e.word)}</a>'
                for e in users[:4]
            )
            endings.append(
                f'<tr><td lang="x-calenha">{html.escape(affix.form)}</td>'
                f"<td>{html.escape(affix.meaning)}</td><td>{examples}</td></tr>"
            )

        body = f"""{self.heading("roots", "The seeds words grow from. A root is never said alone; it waits for an ending.")}
<ul class="roots">{"".join(items)}</ul>
<section class="part doc" aria-labelledby="endings">
<h2 id="endings">endings</h2>
<p>Endings turn roots into words. When an ending that begins with a vowel meets a word
that ends in one, the first vowel gives way: calenha and -i make calenhi.</p>
<div class="table"><table><thead><tr><th>ending</th><th>adds</th><th>as in</th></tr></thead>
<tbody>{"".join(endings)}</tbody></table></div>
</section>"""
        return self.layout(
            "roots — calenha",
            body,
            current="roots.html",
            description="The roots and endings of Calenha.",
        )

    def history(self) -> str:
        language = self.language
        shaped: dict[str, list[Entry]] = {c.name: [] for c in language.sound_changes}
        rows = []
        for entry in self.entries:
            if not entry.old:
                continue
            result = evolve(entry.old, language)
            for step in result.steps:
                shaped[step.change.name].append(entry)
            rows.append(
                f'<tr><td lang="x-calenha">*{html.escape(entry.old)}</td>'
                f'<td lang="x-calenha"><a href="{self.word_path(entry)}">{html.escape(entry.word)}</a></td>'
                f"<td>{html.escape(entry.gloss)}</td></tr>"
            )

        changes = []
        for i, change in enumerate(language.sound_changes, start=1):
            pairs = change.pairs or {change.find: change.replace}
            rule = ", ".join(f"{html.escape(a)} → {html.escape(b)}" for a, b in pairs.items())
            env = environment(change.when)
            env_html = f' <span class="env">{html.escape(env)}</span>' if env else ""
            words = ", ".join(
                f'<a href="{self.word_path(e)}" lang="x-calenha">{html.escape(e.word)}</a>'
                for e in shaped[change.name]
            )
            changes.append(
                f'<li id="c-{i}"><h3>{html.escape(change.name)}</h3>'
                f'<p class="rule" lang="x-calenha">{rule}{env_html}</p>'
                f"<p>{mdown.inline(change.note)}</p>"
                + (f'<p class="shaped">shaped {words}</p>' if words else "")
                + "</li>"
            )

        body = f"""{self.heading("history", "Old Calenha was harder: k, doubled vowels, plain endings. Over many generations the sea air wore it smooth.")}
<p class="doc">These are the changes, in the order they happened. Order matters: the long
vowels formed before n and l softened, which is why *thaliire became thalírë and not
thalhirë.</p>
<ol class="changes">{"".join(changes)}</ol>
<section class="part doc" aria-labelledby="h-old">
<h2 id="h-old">every old form</h2>
<div class="table"><table><thead><tr><th>old</th><th>now</th><th>meaning</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
</section>"""
        return self.layout(
            "history — calenha",
            body,
            current="history.html",
            description="How Old Calenha softened into the modern language.",
        )

    def unspoken(self) -> str:
        language = self.language
        seed = len(language.entries)  # the list changes as the lexicon grows

        def items(candidates) -> str:
            out = []
            for c in candidates:
                echo = (
                    f'<span class="echo">near {", ".join(html.escape(e) for e in c.echoes)}</span>'
                    if c.echoes
                    else ""
                )
                out.append(
                    f'<li><span class="u" lang="x-calenha">{stressed_html(c.word)}</span>'
                    f'<span class="ipa">/{html.escape(c.word.ipa())}/</span>{echo}</li>'
                )
            return "".join(out)

        things = generate(language, n=24, seed=seed, syllables=(2, 3))
        invitations = generate(language, n=12, seed=seed + 1, syllables=(2, 3), kind="verb")
        body = f"""{self.heading("unspoken", "Words the ear has found that mean nothing yet.")}
<div class="doc">
<p>Each of these obeys every rule of the language, and each was chosen by the generator
for how it sounds. None of them has a meaning. To give one, add it to the lexicon in
<code>lang/lexicon/</code>, and it will appear in the dictionary. More can be found with
<code>calenha gen</code>.</p>
</div>
<section class="part" aria-labelledby="h-things">
<h2 id="h-things">things</h2>
<ul class="unspoken">{items(things)}</ul>
</section>
<section class="part" aria-labelledby="h-inv">
<h2 id="h-inv">invitations</h2>
<p class="doc">Verbs, ending in -u, waiting for something to invite.</p>
<ul class="unspoken">{items(invitations)}</ul>
</section>"""
        return self.layout(
            "unspoken — calenha",
            body,
            current="unspoken.html",
            description="Unclaimed Calenha words, waiting for a meaning.",
        )

    def document(self, path: str, source: str, lede: str) -> str:
        text = (self.root / source).read_text(encoding="utf-8")
        doc = mdown.render(text, link=DOC_LINKS.get)
        body = f'{self.heading(doc.title or path.removesuffix(".html"), lede)}\n<div class="doc">{doc.html}</div>'
        current = path if any(href == path for _, href in NAV) else ""
        return self.layout(f"{doc.title} — calenha", body, current=current, description=lede)


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


def build(language: Language, root: Path, out: Path, *, fragment_home: bool = False) -> list[Path]:
    """Write the whole site into ``out``. Returns the files written."""
    site = Site(language, root)
    written = []
    for relative, content in site.pages(fragment_home=fragment_home).items():
        path = out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    css = out / "site.css"
    css.write_text(resources.files(__package__).joinpath("site.css").read_text("utf-8"), "utf-8")
    written.append(css)
    return written


FILTER_SCRIPT = """<script>
(function () {
  var q = document.getElementById("q");
  var count = document.getElementById("count");
  var empty = document.getElementById("empty");
  var entries = Array.prototype.slice.call(document.querySelectorAll(".entry"));
  var letters = Array.prototype.slice.call(document.querySelectorAll(".letter"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  var domain = "";
  function plain(s) {
    return s.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase().trim();
  }
  function apply() {
    var term = plain(q.value);
    var shown = 0;
    entries.forEach(function (e) {
      var ok = (!domain || e.dataset.domain === domain) &&
               (!term || plain(e.dataset.search).indexOf(term) !== -1);
      e.hidden = !ok;
      if (ok) shown++;
    });
    letters.forEach(function (l) { l.hidden = !l.querySelector(".entry:not([hidden])"); });
    count.textContent = shown === 1 ? "1 word" : shown + " words";
    empty.hidden = shown > 0;
  }
  q.addEventListener("input", apply);
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      domain = chip.dataset.domain;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      apply();
    });
  });
})();
</script>"""
