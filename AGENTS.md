# AGENTS.md

Guidance for anyone — human or agent — working in this repository.

## what this is

**Calenha** (*the calm speech*) is a constructed language spoken by the Calenhi of
Solmara, a mythical, unhurried California. It blends the feel of Tolkien's elvish,
the sound of Portuguese with a touch of English, the typographic freedom of
E.E. Cummings, and a very light seasoning of programming-language ideas.

The language is kept as **data** in `lang/`. A small Python toolkit in
`src/calenha/` reads that data, holds it to its own rules, and exports it as JSON.
The website in `web/` (SvelteKit) presents that export. Python owns the rules;
Svelte never re-implements them.

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
  phrases.toml        the language in use, by topic — every word must exist
  texts/*.toml        poems, stories, blessings — line by line, with translations
docs/                 prose reference: phonology, grammar
context/              world, principles, decisions, style
src/calenha/          the toolkit — check, gen, evolve, export
  export.py           the data contract the website reads
tests/                python tests, including checks over the real lexicon
web/                  the website (SvelteKit, Svelte 5, static)
  src/lib/design/     design tokens (primitive → semantic → component) and base styles
  src/lib/components/ ui/, language/ and layout/ components
  src/lib/language/   the contract's types, lookups and the line reader
  src/routes/         one folder per page; /design documents the system
dist/                 generated — never edit by hand
```

## commands

```sh
uv sync                       # install
uv run calenha check          # validate the whole language
uv run calenha show thalírë   # syllables, stress, IPA, etymology
uv run calenha gen -n 12      # coin candidate words, ranked by euphony
uv run calenha evolve kalenia # run an old form through the sound changes
uv run calenha export         # write web/src/lib/data/language.json
uv run calenha build          # export, and write dist/dictionary.md
uv run pytest                 # tests
uv run ruff check . && uv run ruff format --check .

cd web
npm install
npm run dev                   # exports the language, then serves the site
npm run lint && npm run check && npm test
npm run build                 # prerenders every page into web/build
```

`calenha check` must pass before any commit that touches `lang/`.

## working rules

- The data is the truth. Change words in `lang/`, never in `dist/`.
- New words grow from roots where possible. Etymologies must compile exactly.
- Read new words aloud. If a word is correct but not beautiful, it is not done.
- Record any change to the language's rules in `context/decisions.md`.
- Keep the toolkit dependency-free at runtime.
- The website reads only `language.json`. To change a page's words, change its
  source in `lang/`, `docs/` or `context/`; to change how it looks, change `web/`.
- If the export's shape changes, change `src/calenha/export.py` and
  `web/src/lib/language/types.ts` together, and bump `SCHEMA` in both.
- Components use semantic and component tokens only, never primitives or raw
  colours. The one bright colour is `--color-stress`; keep it that way.
- Every push to `main` deploys the site to GitHub Pages (`.github/workflows/pages.yml`).

## git

- Branch per piece of work (`feat/…`, `docs/…`, `fix/…`, `chore/…`, `ci/…`),
  merged into `main` with `--no-ff`.
- Conventional commit messages, lowercase subject.
- Commits are authored by the repository owner. **Do not add AI attribution of any
  kind** — no `Co-Authored-By` trailers, no session links, no "generated with" lines —
  to commits, pull requests or files.
