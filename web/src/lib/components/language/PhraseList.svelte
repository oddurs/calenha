<!--
  @component
  Phrases: the line, its literal reading, and what it means.
-->
<script lang="ts">
	import type { Phrase } from '$lib/language';
	import Line from './Line.svelte';

	let { phrases }: { phrases: Pick<Phrase, 'text' | 'literal' | 'translation'>[] } = $props();
</script>

<ul class="phrases">
	{#each phrases as phrase (phrase.text)}
		<li>
			<p class="cal"><Line text={phrase.text} /></p>
			<p class="literal">{phrase.literal}</p>
			<p class="translation">{phrase.translation}</p>
		</li>
	{/each}
</ul>

<style>
	.phrases {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-m) var(--space-l);
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 20rem), 1fr));
	}
	li {
		min-width: 0;
	}
	.cal {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
	}
	.literal {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		margin-top: var(--space-3xs);
	}
	.translation {
		font-style: italic;
	}
	@media (max-width: 560px) {
		.cal {
			font-size: var(--step-1);
		}
	}
</style>
