<!--
  @component
  A line of Calenha as writing. Words link to their pages and show their meaning on
  hover; the beat stays hidden until then, so the line reads clean. Breaths are set
  apart. With `breathe`, the words arrive one at a time, once.
-->
<script lang="ts">
	import { read } from '$lib/language';
	import { wordHref } from '$lib/links';
	import Word from './Word.svelte';

	interface Props {
		text: string;
		links?: boolean;
		breathe?: boolean;
		beat?: 'always' | 'hover' | 'never';
	}

	let { text, links = true, breathe = false, beat = 'hover' }: Props = $props();
	const tokens = $derived(read(text));
</script>

<span class="line" class:breathe lang="x-calenha"
	>{#each tokens as token, i (i)}{#if i}{' '}{/if}<span class="token" style:--i={i}
			>{#if token.kind === 'breath'}<span class="breath">·</span
				>{:else}{token.lead}{#if token.entry}<Word
						shape={token.entry}
						shown={token.shown}
						href={links ? wordHref(token.entry.slug) : undefined}
						beat={links ? beat : 'never'}
						gloss={links ? token.entry.short : undefined}
					/>{:else}{token.shown}{/if}{token.trail}{/if}</span
		>{/each}</span
>

<style>
	/* the breath: a pause, set smaller and lighter than the words around it */
	.breath {
		color: var(--color-ink-muted);
		font-size: 0.72em;
		padding-inline: 0.1em;
		vertical-align: 0.06em;
	}
	.breathe .token {
		display: inline-block;
		animation: arrive var(--duration-breath) var(--ease-tide) both;
		animation-delay: calc(var(--i) * var(--stagger-breath));
	}
	@keyframes arrive {
		from {
			opacity: 0;
			filter: blur(8px);
			transform: translateY(0.06em);
		}
	}
</style>
