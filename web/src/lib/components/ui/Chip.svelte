<!--
  @component
  A small pill button that can be pressed, for filters and modes.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		pressed?: boolean;
		id?: string;
		title?: string;
		onclick?: () => void;
		children: Snippet;
	}

	let { pressed = false, id, title, onclick, children }: Props = $props();
</script>

<button type="button" class="chip" {id} {title} aria-pressed={pressed} {onclick}>
	{@render children()}
</button>

<style>
	.chip {
		font: inherit;
		font-size: var(--step--1);
		color: var(--color-ink);
		background: transparent;
		border: 1px solid var(--chip-border);
		border-radius: var(--radius-pill);
		padding: 0.15rem 0.8rem;
		cursor: pointer;
		transition:
			border-color var(--duration-quick) var(--ease-tide),
			background-color var(--duration-quick) var(--ease-tide);
	}
	.chip:hover {
		border-color: var(--chip-border-hover);
	}
	.chip[aria-pressed='true'] {
		background: var(--chip-pressed-bg);
		color: var(--chip-pressed-ink);
		border-color: var(--chip-pressed-bg);
	}
</style>
