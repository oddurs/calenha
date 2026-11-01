<!--
  @component
  Phrases: the line in Calenha, its literal reading, and what it means.
-->
<script lang="ts">
	import type { Phrase } from '$lib/language';
	import Line from './Line.svelte';

	interface Props {
		phrases: Pick<Phrase, 'text' | 'literal' | 'translation'>[];
		columns?: 1 | 2;
	}

	let { phrases, columns = 2 }: Props = $props();
</script>

<ul class="phrases" class:two={columns === 2}>
	{#each phrases as phrase (phrase.text)}
		<li>
			<p class="cal"><Line text={phrase.text} /></p>
			<p class="translation">{phrase.translation}</p>
			<p class="literal">{phrase.literal}</p>
		</li>
	{/each}
</ul>

<style>
	.phrases {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-l) var(--space-xl);
	}
	.two {
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 19rem), 1fr));
	}
	li {
		min-width: 0;
		display: grid;
		gap: var(--space-3xs);
		align-content: start;
	}
	.cal {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
		padding-bottom: var(--space-3xs);
	}
	.literal {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
</style>
