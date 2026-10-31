# grammar

Calenha has very little grammar, and every piece of it means something. The words
themselves live in `lang/lexicon/`; the small grammatical words are in
`lang/lexicon/grammar.toml`.

## a sentence is a picture

There is no word for *is*. Things are simply set beside each other:

> **thalírë lenta.** — *river slow.* The river is slow.
>
> **calmarë · ë solenha.** — *now · and dappled-light.* This moment, and the light
> through the leaves.

Adjectives usually follow what they describe (*célë alta*, the high sky), but they
may come first for emphasis (*alta célë* — how high the sky is).

## the one who

Word order is free. To say who is acting, put **lë** before them — like naming an
argument, so it no longer matters where it stands:

> **lë altavel velu.** — the condor wanders.
>
> **velu lë altavel.** — the same, but the wandering comes first in the mind.

Without *lë*, the reader takes the most natural meaning. *Lë* is for when it matters,
and for when the speaker wants to honour the doer.

## every verb is an invitation

Every verb ends in **-u**, and its plain form is an invitation, never a command:

> **velu.** — come wander. *(never: go)*
>
> **calu.** — be still with me.
>
> **nã velu · calu.** — there's no need to wander. Rest.

There is no imperative mood in Calenha, and no way to make one. To ask strongly,
a Calenhi asks again, softer.

## time is a tide

The Calenhi do not have tenses. They have the tide.

| | particle | |
|---|---|---|
| what has gone out | **vaza** (ebb) | *vaza velu* — wandered |
| slack water, now | — | *velu* — wander, wandering |
| what is coming in | **chea** (flood) | *chea velu* — will wander |

> **vaza nevoã · chea solouro.** — the fog has gone out; the golden hour is coming in.

The present needs no marker, because it is where one already stands. When the
present must be named, it is **calmarë** — *still tide*, slack water.

## again and again

**volta** turns an act into a circle:

> **thalírë volta thalu.** — the river flows and flows.

Said alone, *volta* is farewell: *come back around*.

## if, and the breath

**aswen** opens a condition. It holds until the next **breath** — the middle dot
**·** — which closes it, the way a block ends:

> **aswen tu velu · solenha.** — if you wander, there will be light through the leaves.

The breath is a real pause, said as well as written. A line of Calenha breathes.

## wondering, not asking

Questions begin with **sera** — *I wonder*. Calenha doesn't interrogate; it wonders
aloud and leaves room:

> **sera tu escutu marë?** — I wonder: can you hear the tide?

Answer **sí** (yes) or **nã** (no). *Nã* before a word negates it.

To ask *who*, *what*, *where*, *when*, *why* or *how*, put the question word after
*sera*:

| | |
|---|---|
| **cen** | who |
| **cë** | what |
| **ondë** | where — *where the wave is* |
| **candë** | when — answered in tides and seasons, never hours |
| **porcë** | why, and because |
| **como** | how, and like |

> **sera ondë tu velu?** — where are you wandering?
>
> **sera porcë?** — why? **porcë Mar lenta.** — because the sea is slow.

*Porcë* answers itself: every *why* in Calenha already holds its *because*.

## many

Nouns don't change for number. *Onda* is a wave or waves. To make the number felt,
repeat the word:

> **onda onda** — waves, several.
>
> **onda onda onda** — wave after wave after wave; more than can be counted.

## counting

The Calenhi count to ten on their hands, and past ten there is **mil** — *as many
as the waves*, the end of counting.

| | | | | |
|---|---|---|---|---|
| **una** one | **dua** two | **trë** three | **catra** four | **cinca** five |
| **seia** six | **setë** seven | **oita** eight | **novë** nine | **desa** ten |

A number comes before what it counts, and the noun does not change:

> **trë onda** — three waves. **desa una anel** — eleven years (*ten-one rings*).

## whose

Possession is set before the thing held: **minha** (my), **tua** (your), **sua**
(their), **nossa** (our). Or with **dë**, *of*, after it:

> **nossa lar** — our home. **lar dë Calenhi** — the home of the Calenhi.

There is a verb for holding, **tenu**, and none for owning. *ei tenu pão* is "I am
holding bread", never "the bread is mine".

## more and less

**mais** (more) and **menos** (less) follow the quality they change:

> **célë alta mais** — the sky, higher. **lenta mais · lenta mais** — slower, slower.

## courtesy

There is no word for *please*. Every verb is already an invitation, so a request
is polite simply by being made in Calenha. To thank someone, say **salva** — the
same word as *sage*, whose smoke is given as thanks. To ask forgiveness, **perdão**.

> **venha, venida.** — welcome, guest. **salva, amiga.** — thank you, friend.

## colour

Colours are named for the things that wear them, with **-osa**, *full of*:
**célosa** (sky-full, blue), **algosa** (kelp-full, green), **ardosa** (fire-full,
red), **ourosa** (gold-full), **nevosa** (fog-full, grey), **alvosa** (dawn-full,
white), **noitosa** (night-full, dark).

## the remembered

There is no verb for dying. One becomes **mirida** — *the remembered*:

> **ela chea mirida.** — they will be remembered. *(they are dying)*

## capitals are a bow

Calenha is written in lowercase. A **Capital** is not spelling; it is reverence.
The sea is *mar*; the Sea, as an elder, is *Mar*. A redwood is *miraluma*; the old
redwood who remembers is *Miraluma*.

> **lë Miraluma miru.** — the redwood remembers.

A capital may be given to anything — a person, a stone, a morning — that the speaker
wishes to honour.

## the broken word

A breath inside a word breaks it open. The word keeps its meaning, but now it aches:

> **mirão** — memory. **mi·rão** — a memory that hurts to hold.
>
> **mi·rão dë lar** — the ache of remembering home.

Use it rarely. It is the strongest thing the language can do.

## building words

Words grow from roots (`lang/roots.toml`) with endings (`lang/affixes.toml`):

| ending | adds | example |
|---|---|---|
| -u | the invitation (verb) | *vel* wander → **velu** |
| -unda | the going-about of it | **velunda**, a wandering |
| -a | the plain thing, or a quality | *ond* → **onda**, wave; *alt* → **alta**, high |
| -ë | the rhythm of it | *mar* → **marë**, tide; *ard* → **ardë**, fire |
| -ão | a thing held inside | *mir* → **mirão**, memory |
| -oã | a soft visiting presence | *nev* → **nevoã**, sea fog |
| -inha | little, dear | *our* → **ourinha**, poppy (little gold) |
| -essa | a field of | *our* → **ouressa**, poppy field |
| -írë | the ever- | *thal* → **thalírë**, river (the ever-flowing) |
| -enha | the speech of | *sol* → **solenha**, dappled light |
| -i | the people of | **calenha** → **calenhi** |
| -eira | one who does it | *cant* → **canteira**, singer; *vel* → **veleira**, sailboat |
| -ida | one to whom it was done | *ven* → **venida**, guest; *mir* → **mirida**, the remembered |
| -al | a place where it gathers | *pinh* → **pinhal**, pine wood; *ond* → **ondal**, surf |
| -osa | full of; the colour of | *nev* → **nevosa**, grey; *lum* → **lumosa**, luminous |
| vol- | back, around again | **venu** → **volvenu**, to return |

Roots join into names, often with a linking **-a-**: *alt-a-vel*, the high
wanderer — the condor. When a vowel-initial ending meets a vowel, the first vowel
gives way: *calenha + -i* → *calenhi*.
