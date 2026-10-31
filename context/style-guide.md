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
