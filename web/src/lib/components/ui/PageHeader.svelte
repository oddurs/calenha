<!--
  @component
  The title of a page, with an optional line beneath it.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		lede?: string;
		/** set to 'x-calenha' when the title is in Calenha */
		lang?: string;
		children?: Snippet;
	}

	let { title, lede, lang, children }: Props = $props();
</script>

<header class="head">
	<h1 {lang}>{title}</h1>
	{#if lede}<p class="lede">{lede}</p>{/if}
	{@render children?.()}
</header>

<style>
	.head {
		display: grid;
		gap: var(--space-xs);
		padding-block: var(--space-l) var(--space-m);
	}
	h1 {
		font-size: var(--step-4);
		line-height: 1.05;
		letter-spacing: -0.01em;
	}
	.lede {
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step-1);
		max-width: var(--measure-text);
	}
</style>
