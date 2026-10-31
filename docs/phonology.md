# phonology

*How Calenha sounds, and how it is written.* The machine-readable version of this
page is `lang/phonology.toml`; if the two disagree, the TOML wins and this page is
out of date.

## vowels

Five plain vowels, open and unhurried as in Portuguese:

| letter | sound | like |
|---|---|---|
| a | [a] | *father*, short |
| e | [ɛ] | *bed* |
| i | [i] | *machine* |
| o | [ɔ] | *thought* |
| u | [u] | *rule* |

**ë** is an *e* at the very end of a word, said as a clear [e]. A word may never end
in a plain *e*, and *ë* appears nowhere else. On the page it gives an ending a small
lift: *thalírë*, *miralë*.

**The acute** (á é í ó ú) marks a long, held vowel. A long vowel always takes the
stress. Use it rarely, where a word wants to linger: *tha-LÍÍ-rë*, the river.

**The tilde** marks a nasal vowel: *ã*, *õ*, and the glides *ão*, *ãe*, *õe*. These are
the Portuguese heart of the language — *mirão*, memory; *nevoã*, the fog.

**Glides** — *ai, au, ei, eu, oi, ou* — are each one syllable: *so-LOU-ro*.

## consonants

| | letters |
|---|---|
| soft stops | p b t d c g — *c* and *g* are always hard |
| breath | f v s z th — *th* as in *thin* |
| hush | ch [ʃ], j [ʒ] |
| hum | m n nh [ɲ] |
| flow | l lh [ʎ] r w |

*r* is a light tap, as in Spanish *pero*. Two *r*s across a syllable break make a
trill. A single *s* between vowels softens to [z] (*bri-SAL-ma* is [bɾiˈzalma]); write
*ss* to keep it sharp (*ouressa*).

*lh* and *nh* never begin a word. They live in the middle, where they are softest.

## syllables

A syllable is: an optional onset, a vowel, and an optional closing consonant.

- **onsets** — any single consonant, or a stop or *f* followed by *l* or *r*
  (*pl pr bl br tr dr cl cr gl gr fl fr*), or *thr*.
- **inside a word**, a syllable may close with *m n l r s*.
- **at the end of a word**, only *n l r s* — the soft ones. Most words end in a vowel.

Between two vowels, consonants join the following syllable whenever they can begin
one: *pe-dral-ta*, not *ped-ral-ta*.

## stress

Stress rests on the **second-to-last syllable**: *ca-LE-nha*, *al-GA-mar*,
*mi-ra-LU-ma*. Two things move it, and both can be seen in the spelling:

1. a word that ends in a **nasal** draws stress to its end: *mi-RÃO*, *ne-vo-Ã*.
2. a **long vowel** always takes the stress: *tha-LÍ-rë*.

## the breath mark

The middle dot **·** is not a sound but a silence. See `docs/grammar.md`.
