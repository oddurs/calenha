<!--
  @component
  A line read word by word: each word above its short meaning.
-->
<script lang="ts">
	import { read } from '$lib/language';
	import { wordHref } from '$lib/links';
	import Word from './Word.svelte';

	interface Props {
		text: string;
		size?: 'normal' | 'large';
	}

	let { text, size = 'normal' }: Props = $props();
	const tokens = $derived(read(text));
</script>

<span class="interlinear {size}">
	{#each tokens as token, i (i)}
		{#if token.kind === 'breath'}
			<span class="cell pause"><span class="w">·</span><span class="g">pause</span></span>
		{:else if token.entry}
			<span class="cell">
				<span class="w"
					><Word shape={token.entry} shown={token.shown} href={wordHref(token.entry.slug)} /></span
				>
				<span class="g">{token.entry.short}{token.aching ? ' (aching)' : ''}</span>
			</span>
		{:else}
			<span class="cell unknown"
				><span class="w" lang="x-calenha">{token.shown}</span><span class="g">not yet a word</span
				></span
			>
		{/if}
	{/each}
</span>

<style>
	.interlinear {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-s);
		align-items: flex-start;
	}
	.cell {
		display: inline-grid;
	}
	.w {
		font-size: var(--step-1);
		line-height: var(--leading-snug);
	}
	.large .w {
		font-size: var(--step-2);
	}
	.g {
		font-size: var(--step--2);
		font-style: italic;
		color: var(--color-ink-muted);
		line-height: var(--leading-snug);
	}
	.pause .w,
	.unknown .w {
		color: var(--color-ink-muted);
	}
	.unknown {
		opacity: 0.75;
	}
</style>
