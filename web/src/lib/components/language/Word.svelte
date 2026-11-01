<!--
  @component
  A Calenha word. Its stressed syllable carries the beat: a short poppy bar above
  it, the design system's one bright mark.

  beat: 'always' where a word stands alone (headwords, glosses, the reader);
        'hover' in running lines, where marks would crowd the writing;
        'never' for words that are names of things on the page.
  gloss: shown on hover or focus, for linked words in lines.
-->
<script lang="ts">
	import { stressSpans, type Shape } from '$lib/language';

	interface Props {
		shape: Pick<Shape, 'syllables' | 'stress'>;
		/** the word as written, if it differs from the dictionary form (capitals, breaths) */
		shown?: string;
		href?: string;
		beat?: 'always' | 'hover' | 'never';
		gloss?: string;
	}

	let { shape, shown, href, beat = 'always', gloss }: Props = $props();
	const spans = $derived(stressSpans(shape, shown ?? shape.syllables.join('')));
</script>

{#snippet breathe(text: string)}{#each text.split('·') as piece, i (i)}{#if i}<span class="breath"
				>·</span
			>{/if}{piece}{/each}{/snippet}

{#snippet body()}{@render breathe(spans.before)}{#if spans.stressed}<span class="stress"
			>{spans.stressed}</span
		>{/if}{@render breathe(spans.after)}{/snippet}

{#if href}
	<a class="word beat-{beat}" {href} lang="x-calenha"
		>{@render body()}{#if gloss}<span class="gloss" lang="en">{gloss}</span>{/if}</a
	>
{:else}
	<span class="word beat-{beat}" lang="x-calenha">{@render body()}</span>
{/if}

<style>
	.word {
		position: relative;
		color: inherit;
		text-decoration: none;
		border-radius: var(--radius-s);
		transition: background-color var(--duration-quick) var(--ease-tide);
	}
	a.word:hover,
	a.word:focus-visible {
		background: color-mix(in srgb, var(--color-ink) 7%, transparent);
	}

	.stress {
		position: relative;
	}
	/* the beat spans its syllable, just above the tallest letters and accents */
	.stress::before {
		content: '';
		position: absolute;
		left: var(--beat-inset);
		right: var(--beat-inset);
		bottom: calc(100% - var(--beat-drop));
		min-width: 0.3em;
		height: var(--beat-thickness);
		background: var(--beat-color);
		border-radius: 1px;
		opacity: 0;
		transition: opacity var(--duration-quick) var(--ease-tide);
	}
	.beat-always .stress::before,
	.beat-hover:hover .stress::before,
	.beat-hover:focus-visible .stress::before {
		opacity: 1;
	}

	.breath {
		color: var(--color-ink-muted);
		font-size: 0.72em;
		padding-inline: 0.04em;
		vertical-align: 0.06em;
	}

	.gloss {
		position: absolute;
		left: 50%;
		top: calc(100% + 0.3rem);
		translate: -50% -0.2rem;
		z-index: 5;
		font-family: var(--font-english);
		font-size: var(--step--1);
		font-style: italic;
		font-weight: 400;
		line-height: 1.2;
		letter-spacing: 0;
		white-space: nowrap;
		color: var(--color-page);
		background: var(--color-ink);
		padding: 0.3rem 0.6rem;
		border-radius: var(--radius-s);
		opacity: 0;
		pointer-events: none;
		transition:
			opacity var(--duration-quick) var(--ease-tide),
			translate var(--duration-quick) var(--ease-tide);
	}
	a.word:hover .gloss,
	a.word:focus-visible .gloss {
		opacity: 1;
		translate: -50% 0;
	}
</style>
