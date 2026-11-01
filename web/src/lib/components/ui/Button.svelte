<!--
  @component
  A quiet button, for the few actions the site has.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	let { onclick, children }: { onclick: () => void; children: Snippet } = $props();
</script>

<button type="button" {onclick}>{@render children()}</button>

<style>
	button {
		font: inherit;
		font-size: var(--step--1);
		font-weight: 500;
		color: var(--color-ink);
		background: transparent;
		border: var(--rule);
		border-radius: var(--radius-m);
		padding: 0.35rem 0.85rem;
		cursor: pointer;
		transition: background-color var(--duration-quick) var(--ease-tide);
	}
	button:hover {
		background: var(--color-surface);
	}
</style>
