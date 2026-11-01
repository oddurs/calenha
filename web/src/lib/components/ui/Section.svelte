<!--
  @component
  A titled part of a page. The title sits in the margin; the content in the main
  column. With `wide`, the content spans both.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		id: string;
		title: string;
		lang?: string;
		wide?: boolean;
		children: Snippet;
	}

	let { id, title, lang, wide = false, children }: Props = $props();
</script>

<section class="section margined" class:wide aria-labelledby={id}>
	<h2 class="margin" {id} {lang}>{title}</h2>
	<div class="main">{@render children()}</div>
</section>

<style>
	.section {
		padding-top: var(--space-xl);
		row-gap: var(--space-m);
		scroll-margin-top: var(--space-m);
	}
	h2 {
		font-size: var(--step-0);
		font-weight: 500;
		line-height: 1.4;
		padding-top: 0.3rem;
		color: var(--color-ink);
	}
	h2:lang(x-calenha) {
		font-size: var(--step-1);
		padding-top: 0;
	}
	.main {
		display: grid;
		gap: var(--space-m);
	}
	.wide > h2,
	.wide > .main {
		grid-column: 1 / -1;
	}
	@media (min-width: 761px) {
		h2 {
			position: sticky;
			top: var(--space-m);
			align-self: start;
		}
	}
</style>
