# calenha

> **tardë morna · brisa fria · Mar lenta.**
> *A warm afternoon, a cool breeze, the slow sea.*

**Calenha** — *the calm speech* — is a constructed language spoken by the Calenhi of
Solmara, a California one step to the side of ours, where nothing was ever hurried.

It sounds like Portuguese with a touch of English, feels like Tolkien's elvish, takes
the typographic freedom of E.E. Cummings seriously, and keeps a quiet seasoning of
programming-language ideas.

## five things to know

- **every verb is an invitation.** Verbs end in *-u*, and there is no command form.
  *velu* is "come wander", never "go".
- **time is a tide.** *vaza* (ebb) marks what has passed, *chea* (flood) what is
  coming. Now is slack water, *calmarë*, and needs no marker.
- **a space can be a silence.** The breath mark **·** is a pause that closes a
  condition, the way a block ends. Inside a word it makes the word ache:
  *mirão*, memory; *mi·rão*, a memory that hurts to hold.
- **capitals are a bow.** Everything is lowercase; a Capital is reverence.
  *lë Miraluma miru* — the redwood remembers.
- **words grow from roots.** *thal* (flow) + *-írë* (the ever-) gives *thalírë*, river.
  *alt* (high) + *vel* (wander) gives *altavel*, the condor.

## the language is data

Everything about Calenha lives in [`lang/`](lang) as plain TOML: the sounds, the roots,
the endings, the words, the phrases and the language's own history. A small Python
toolkit reads it, holds it to its rules, and builds a dictionary.

```sh
uv sync
uv run calenha check            # 122 words, 34 roots — does everything obey the rules?
uv run calenha show thalírë     # tha·LÍ·rë  /θa.ˈliː.ɾe/  river, from thal + -írë
uv run calenha read "aswen tu velu · solenha."
uv run calenha gen -n 12        # coin new words, the most euphonious first
uv run calenha evolve kalenia   # *kalenia → calenia → calenha
uv run calenha build            # the website, into dist/
uv run calenha serve            # preview it at http://127.0.0.1:8000
```

## the website

`calenha build` turns the language into a small static site: a page for every word
(with its parts, its history and its family), the roots and endings, the grammar, the
sounds, a phrasebook, longer texts you can read with a translation or word by word, a
reader that glosses any line you paste in, the history of Old Calenha, the world, and a
page of *unspoken* words — ones the generator has found that mean nothing yet. Every push to `main` publishes it to
GitHub Pages.

## start here

| | |
|---|---|
| [`context/world.md`](context/world.md) | Solmara and the Calenhi |
| [`context/principles.md`](context/principles.md) | what must never be lost |
| [`docs/phonology.md`](docs/phonology.md) | how it sounds and is written |
| [`docs/grammar.md`](docs/grammar.md) | how it works |
| [`context/decisions.md`](context/decisions.md) | what was decided, and why |
| [`AGENTS.md`](AGENTS.md) | how to work in this repository |
