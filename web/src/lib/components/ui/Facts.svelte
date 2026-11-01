<!--
  @component
  Labelled facts, each on its own row: the label in the margin, the fact beside it.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	let { facts }: { facts: { label: string; body: Snippet }[] } = $props();
</script>

<dl class="facts">
	{#each facts as fact (fact.label)}
		<div class="fact margined">
			<dt class="margin">{fact.label}</dt>
			<dd class="main">{@render fact.body()}</dd>
		</div>
	{/each}
</dl>

<style>
	.fact {
		padding-block: var(--space-m);
		border-top: var(--rule);
		row-gap: var(--space-2xs);
	}
	dt {
		color: var(--color-ink-muted);
		padding-top: 0.2rem;
	}
	dd {
		display: grid;
		gap: var(--space-xs);
	}
</style>
