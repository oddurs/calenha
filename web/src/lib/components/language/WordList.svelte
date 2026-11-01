<!--
  @component
  A run of words, each linked, each with its meaning beside it.
-->
<script lang="ts">
	import { entry } from '$lib/language';
	import { wordHref } from '$lib/links';

	interface Props {
		slugs: string[];
		gloss?: boolean;
	}

	let { slugs, gloss = true }: Props = $props();
	const words = $derived(slugs.map(entry).filter((e) => e !== undefined));
</script>

<ul class="words" class:bare={!gloss}>
	{#each words as w (w.slug)}
		<li>
			<a href={wordHref(w.slug)} lang="x-calenha">{w.word}</a>{#if gloss}<span class="g"
					>{w.short}</span
				>{/if}
		</li>
	{/each}
</ul>

<style>
	.words {
		list-style: none;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-m);
	}
	.bare {
		gap: var(--space-3xs) var(--space-s);
	}
	li {
		display: inline-flex;
		align-items: baseline;
		gap: 0.4em;
	}
	a {
		font-size: 1.12em;
		text-decoration: none;
	}
	a:hover {
		text-decoration: underline;
		text-decoration-color: var(--color-accent);
	}
	.g {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		font-style: italic;
	}
</style>
