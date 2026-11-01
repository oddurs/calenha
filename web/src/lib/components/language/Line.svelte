<!--
  @component
  A line of Calenha. Every word shows its stress and links to its own page;
  breaths are set apart. With `breathe`, the words arrive one at a time, once.
-->
<script lang="ts">
	import { read } from '$lib/language';
	import { wordHref } from '$lib/links';
	import Word from './Word.svelte';

	interface Props {
		text: string;
		links?: boolean;
		breathe?: boolean;
	}

	let { text, links = true, breathe = false }: Props = $props();
	const tokens = $derived(read(text));
</script>

<span class="line" class:breathe lang="x-calenha">
	{#each tokens as token, i (i)}
		{#if i}{' '}{/if}<span class="token" style:--i={i}
			>{#if token.kind === 'breath'}<span class="breath">·</span
				>{:else}{token.lead}{#if token.entry}<Word
						shape={token.entry}
						shown={token.shown}
						href={links ? wordHref(token.entry.slug) : undefined}
					/>{:else}{token.shown}{/if}{token.trail}{/if}</span
		>
	{/each}
</span>

<style>
	.breath {
		color: var(--color-ink-muted);
	}
	.breathe .token {
		display: inline-block;
		animation: arrive var(--duration-breath) var(--ease-tide) both;
		animation-delay: calc(var(--i) * var(--stagger-breath));
	}
	@keyframes arrive {
		from {
			opacity: 0;
			filter: blur(6px);
			transform: translateY(0.08em);
		}
	}
</style>
