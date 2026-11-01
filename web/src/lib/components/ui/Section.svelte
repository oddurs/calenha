<!--
  @component
  A titled part of a page.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		id: string;
		title: string;
		children: Snippet;
	}

	let { id, title, children }: Props = $props();
</script>

<section aria-labelledby={id}>
	<h2 {id}>{title}</h2>
	{@render children()}
</section>

<style>
	section {
		padding-top: var(--space-xl);
		display: grid;
		gap: var(--space-m);
		scroll-margin-top: var(--space-m);
	}
	h2 {
		font-size: var(--step-2);
		color: var(--color-accent);
	}
</style>
