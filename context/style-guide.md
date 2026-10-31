# style guide

How to write entries so the dictionary reads as one voice.

## headwords

- Lowercase, always. Capitals are grammar, not spelling (see `docs/grammar.md`).
- Spelled exactly as the phonology allows. `calenha check` is the judge.
- Final *e* is always written *ë*.

## glosses

- The **gloss** is short and literal: one to four words, lowercase, no full stop.
  `river`, `to wander`, `golden hour`.
- The **sense** (optional) is the poetic meaning, one sentence, written the way a
  Calenhi might explain it to a traveller.
  *"the ever-flowing; a river is called by what it does."*
- Avoid English idiom in glosses. Prefer the plain thing.

## etymology

- Every derived word lists its morphemes in order, and they must compile to the
  headword exactly. Roots are bare (`mir`), affixes carry hyphens (`-ão`, `-a-`).
- Words coined from nothing have no `from`; give them a root in `roots.toml` if they
  are likely to have children.
- Old forms (`old`) are written with an asterisk in prose (*\*kalenia*) but stored
  without it. They must evolve into the headword through `lang/sound-changes.toml`.

## choosing new words

1. Is there a root? Build from it.
2. If not, run `calenha gen` and read the candidates aloud.
3. Check that the word doesn't collide in sound with an existing word of a
   different meaning.
4. Ask: does it feel like late afternoon on a headland?

## texts

- A text lives in `lang/texts/<slug>.toml`: a Calenha `title`, an `english` title, a
  `kind` (poem, story, blessing), a `note` for the reader, and its lines.
- Each line has its Calenha `text` and an English `translation`. An empty line is a
  stanza break. Word-by-word glosses are generated from the dictionary, so a text
  never repeats what the lexicon already knows.
- Write the translation as English a person would say, not a gloss.
- Use the breath mark and the bow (capitals) where they mean something. A text is
  where the language's typography should be most alive.
- If a text needs a word that doesn't exist, grow it in the lexicon first.

## phrases

- Every phrase has a `topic`: greetings, the hours, the heart, land and sea, or
  sayings. Keep the literal line word-for-word, joined with hyphens where one Calenha
  word needs several English ones.
