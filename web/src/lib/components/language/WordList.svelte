<!--
  @component
  A run of words, each linked, each with its meaning in small italics.
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

<ul class="words">
	{#each words as w (w.slug)}
		<li>
			<a href={wordHref(w.slug)} lang="x-calenha">{w.word}</a>{#if gloss}{' '}<i>{w.short}</i>{/if}
		</li>
	{/each}
</ul>

<style>
	.words {
		list-style: none;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3xs) var(--space-m);
	}
	i {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
</style>
