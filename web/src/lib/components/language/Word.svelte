<!--
  @component
  A Calenha word with its stressed syllable marked in poppy gold, with a hairline
  beat beneath. The design system's one bright accent.
-->
<script lang="ts">
	import { stressSpans, type Shape } from '$lib/language';

	interface Props {
		shape: Pick<Shape, 'syllables' | 'stress'>;
		/** the word as written, if it differs from the dictionary form (capitals, breaths) */
		shown?: string;
		href?: string;
	}

	let { shape, shown, href }: Props = $props();
	const spans = $derived(stressSpans(shape, shown ?? shape.syllables.join('')));
</script>

{#snippet body()}{@render breathe(spans.before)}{#if spans.stressed}<span class="stress"
			>{spans.stressed}</span
		>{/if}{@render breathe(spans.after)}{/snippet}

{#snippet breathe(text: string)}{#each text.split('·') as piece, i (i)}{#if i}<span class="breath"
				>·</span
			>{/if}{piece}{/each}{/snippet}

{#if href}
	<a class="word" {href} lang="x-calenha">{@render body()}</a>
{:else}
	<span class="word" lang="x-calenha">{@render body()}</span>
{/if}

<style>
	.word {
		text-decoration: none;
		border-radius: var(--radius-s);
	}
	a.word:hover {
		background: var(--color-surface);
	}
	.stress {
		color: var(--stress-color);
		text-decoration: underline;
		text-decoration-thickness: max(var(--stress-rule), 0.03em);
		text-underline-offset: var(--stress-offset);
	}
	.breath {
		color: var(--color-ink-muted);
		padding-inline: 0.06em;
	}
</style>
