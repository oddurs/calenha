<!--
  @component
  A list of labelled facts, each on its own hairline row.
  Pass `facts` as label/snippet pairs; empty ones are skipped by the caller.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		facts: { label: string; body: Snippet }[];
	}

	let { facts }: Props = $props();
</script>

<dl class="facts">
	{#each facts as fact (fact.label)}
		<div class="fact">
			<dt>{fact.label}</dt>
			<dd>{@render fact.body()}</dd>
		</div>
	{/each}
</dl>

<style>
	.facts {
		margin: var(--space-l) 0 0;
		border-top: var(--rule);
	}
	.fact {
		display: grid;
		grid-template-columns: minmax(0, 9rem) minmax(0, 1fr);
		gap: var(--space-3xs) var(--space-m);
		padding-block: var(--space-s);
		border-bottom: var(--rule);
	}
	dt {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		padding-top: 0.25rem;
	}
	dd {
		margin: 0;
		min-width: 0;
		display: grid;
		gap: var(--space-2xs);
	}
	@media (max-width: 560px) {
		.fact {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
