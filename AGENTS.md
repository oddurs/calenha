# AGENTS.md

Guidance for anyone — human or agent — working in this repository.

## what this is

**Calenha** (*the calm speech*) is a constructed language spoken by the Calenhi of
Solmara, a mythical, unhurried California. It blends the feel of Tolkien's elvish,
the sound of Portuguese with a touch of English, the typographic freedom of
E.E. Cummings, and a very light seasoning of programming-language ideas.

The language is kept as **data** in `lang/`. A small Python toolkit in
`src/calenha/` reads that data, holds it to its own rules, and builds a readable
dictionary.

Before changing anything about the language itself, read:

1. `context/world.md` — who speaks it, and where
2. `context/principles.md` — what must never be lost
3. `context/decisions.md` — what has been decided, and why
4. `context/style-guide.md` — how entries are written

## layout

```
lang/                 the language — source of truth (TOML)
  phonology.toml      sounds, spelling, syllables, stress
  roots.toml          roots words grow from
  affixes.toml        suffixes and linking vowels
  sound-changes.toml  old Calenha → modern Calenha
  lexicon/*.toml      words, one file per domain (grammar.toml: the small words)
  phrases.toml        the language in use — every word must exist
docs/                 prose reference: phonology, grammar
context/              world, principles, decisions, style
src/calenha/          the toolkit
tests/                tests, including checks over the real lexicon
dist/                 generated — never edit by hand
```

## commands

```sh
uv sync                       # install
uv run calenha check          # validate the whole language
uv run calenha show thalírë   # syllables, stress, IPA, etymology
uv run calenha gen -n 12      # coin candidate words, ranked by euphony
uv run calenha evolve kalenia # run an old form through the sound changes
uv run calenha build          # write dist/dictionary.md and dist/index.html
uv run pytest                 # tests
uv run ruff check . && uv run ruff format --check .
```

`calenha check` must pass before any commit that touches `lang/`.

## working rules

- The data is the truth. Change words in `lang/`, never in `dist/`.
- New words grow from roots where possible. Etymologies must compile exactly.
- Read new words aloud. If a word is correct but not beautiful, it is not done.
- Record any change to the language's rules in `context/decisions.md`.
- Keep the toolkit dependency-free at runtime.

## git

- Branch per piece of work (`feat/…`, `docs/…`, `fix/…`, `chore/…`, `ci/…`),
  merged into `main` with `--no-ff`.
- Conventional commit messages, lowercase subject.
- Commits are authored by the repository owner. **Do not add AI attribution of any
  kind** — no `Co-Authored-By` trailers, no session links, no "generated with" lines —
  to commits, pull requests or files.
