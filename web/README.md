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

- `src/lib/design/tokens.css` — every value, in three layers: **primitives** (fog,
  pacific, sage, rose, amber, poppy), **semantic** roles set once per **hour**, and
  **component** decisions recomputed wherever an hour is set.
- `src/lib/design/hours.ts` — the five hours and `pickHour`, whose source is inlined
  into every page by `src/hooks.server.ts` so the hour is set before first paint.
- `src/lib/design/base.css` — element defaults, the two voices keyed to `lang`, and
  the margin grid (`.margined` with `.margin` and `.main`).
- `src/lib/sections.ts` — the four sections and their pages, each named in Calenha.
- `src/lib/components/` — `ui/` (Tabs, Button, SearchField, PageHeader, Section,
  Facts, LinkList, Prose, DocPage), `language/` (Word, Line, Interlinear, EntryRow,
  PhraseList, WordList), `layout/` (SiteHeader, SectionNav, SiteFooter,
  HourControl, Horizon, Meta, SkipLink).

The rules: components use semantic and component tokens, never primitives or raw
colours. Calenha is tagged `lang="x-calenha"` and the type follows. Siblings are
spaced with `gap`. The only bright colour is the beat, and it only marks stress.

All of it is documented live at `/design`, where each hour is shown as the real
token set applied to a part of the page.
