# web

The Calenha website. SvelteKit 2, Svelte 5, prerendered to static files.

```sh
npm install
npm run dev        # exports the language from ../lang, then serves
npm run build      # prerenders every page into build/
npm run lint       # prettier + eslint
npm run check      # svelte-check, strict, warnings fail
npm test           # vitest
```

`npm run dev` and `npm run build` run `calenha export` first, so Python and
[uv](https://docs.astral.sh/uv/) need to be installed. Set `BASE_PATH` when serving
from a subfolder (CI sets it for GitHub Pages).

## how it fits together

```
../lang/*.toml ──calenha export──▶ src/lib/data/language.json  (generated)
                                          │
                       src/lib/language/  ▼  types, lookups, the line reader
                                          │
                     src/lib/components/  ▼  ui · language · layout
                                          │
                            src/routes/   ▼  one folder per page
```

The site never knows the language's rules, only what they produced: syllables,
stress, IPA, glosses, families, histories. Change the contract in
`../src/calenha/export.py` and `src/lib/language/types.ts` together.

## design system

- `src/lib/design/tokens.css` — every value, in three layers: **primitives** (the
  palette and scales, named for Solmara), **semantic** roles (the only layer that
  changes with the theme), and **component** decisions.
- `src/lib/design/base.css` — element defaults, from semantic tokens only.
- `src/lib/design/tokens.ts` — names and notes for each token, for the docs page.
- `src/lib/components/` — `ui/` (Chip, ChipGroup, SearchField, PageHeader, Section,
  Facts, LinkList, Prose, DocPage, ThemeToggle), `language/` (Word, Line,
  Interlinear, EntryRow, PhraseList, WordList), `layout/` (header, footer, meta).

The rules: components use semantic and component tokens, never primitives or raw
colours. Siblings are spaced with `gap`. The only bright colour is
`--color-stress`, and it only ever marks a stressed syllable.

All of it is documented live at `/design`.
