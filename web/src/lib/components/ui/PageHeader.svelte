<!--
  @component
  A page's name, twice: in English in the margin, where you look to find your way,
  and in Calenha across the page, where you look to read. The Calenha title is a
  word from the dictionary, so it shows its beat and links to its page.
-->
<script lang="ts">
	import Word from '$components/language/Word.svelte';
	import { lookup } from '$lib/language';
	import { wordHref } from '$lib/links';

	interface Props {
		english: string;
		/** a Calenha word; if it is in the dictionary, it links there */
		calenha: string;
		lede?: string;
	}

	let { english, calenha, lede }: Props = $props();
	const entry = $derived(lookup(calenha));
</script>

<header class="head margined">
	<p class="margin english">{english}</p>
	<div class="main">
		<h1>
			{#if entry}
				<Word shape={entry} href={wordHref(entry.slug)} />
			{:else}
				<span lang="x-calenha">{calenha}</span>
			{/if}
		</h1>
		{#if entry}<p class="means">{calenha} means <i>{entry.short}</i></p>{/if}
		{#if lede}<p class="lede">{lede}</p>{/if}
	</div>
</header>

<style>
	.head {
		padding-block: var(--space-xl) var(--space-l);
		align-items: baseline;
	}
	.english {
		font-size: var(--step-1);
		font-weight: 500;
		color: var(--color-ink);
	}
	.main {
		display: grid;
		gap: var(--space-2xs);
	}
	h1 {
		font-size: var(--step-5);
		line-height: var(--leading-display);
		letter-spacing: -0.01em;
	}
	.means {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.means i {
		color: var(--color-ink);
	}
	.lede {
		font-size: var(--step-1);
		line-height: var(--leading-snug);
		max-width: 30em;
		padding-top: var(--space-xs);
	}
	@media (max-width: 760px) {
		.head {
			padding-top: var(--space-l);
			row-gap: var(--space-2xs);
		}
		.english {
			font-size: var(--step-0);
			color: var(--color-ink-muted);
		}
	}
</style>
