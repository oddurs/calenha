# decisions

A running log. Newest at the bottom. Each entry: what was decided, and why.

### D-001 · the language is data; the code is a compiler
All language content lives in TOML under `lang/`. The Python toolkit reads it,
validates it and renders it. Like a design system: tokens are the source of truth;
everything else is generated.

### D-002 · python, zero runtime dependencies
Python 3.11+ for `tomllib` in the standard library. Quick to change while the
language is still finding itself. Dev tools (pytest, ruff) via `uv`.

### D-003 · stress rests on the second-to-last syllable
The Portuguese music. Two exceptions, both audible in the spelling:
a word ending in a nasal (*mirão*, *nevoã*) draws stress to its end, and an acute
accent marks a long vowel, which always takes the stress (*thalírë*).

### D-004 · c is always /k/
As in Quenya. There is no soft *c* and no letter *k* in the modern spelling; *k*
survives only in old forms.

### D-005 · final e is written ë
Borrowed from Tolkien. It reminds the reader the vowel is sounded, and it gives
word-endings a little lift on the page. A plain *e* may not end a word, and *ë* may
appear nowhere else.

### D-006 · digraphs ch, lh, nh, th
*ch* /ʃ/, *lh* /ʎ/, *nh* /ɲ/ from Portuguese; *th* /θ/ from English. *lh* and *nh*
never begin a word, as in Portuguese, which keeps them soft and medial.

### D-007 · no imperative mood
The plain verb is an invitation. See `context/principles.md` §6.

### D-008 · tense is a tide
Past and future are marked by the particles *vaza* (ebb) and *chea* (flood);
the present, slack water, is unmarked. From Portuguese *vazante* and *cheia*.

### D-009 · the breath mark ·
A middle dot. Between words it is a pause that closes the scope of a particle
(the language's quiet nod to a block ending). Inside a word it breaks the word open
with longing: *mi·rão*, "a memory that hurts to hold".

### D-010 · the land is Solmara, the people the Calenhi
*Solmara*, sun and sea. *Calenhi*, the calm ones, formed from *calenha* by the
people-suffix *-i*.
