<!--
  @component
  Hairline rows that each lead somewhere, with a name and a short note.
-->
<script lang="ts">
	interface Item {
		label: string;
		href: string;
		note: string;
		lang?: string;
	}

	let { items }: { items: Item[] } = $props();
</script>

<ul class="links">
	{#each items as item (item.href)}
		<li>
			<a href={item.href}>
				<b lang={item.lang}>{item.label}</b>
				<span>{item.note}</span>
			</a>
		</li>
	{/each}
</ul>

<style>
	.links {
		list-style: none;
		padding: 0;
		border-top: var(--rule);
	}
	li {
		border-bottom: var(--rule);
	}
	a {
		display: grid;
		grid-template-columns: minmax(0, 9rem) minmax(0, 1fr);
		gap: var(--space-3xs) var(--space-m);
		padding-block: var(--space-s);
		text-decoration: none;
	}
	b {
		font-weight: 400;
		font-size: var(--step-1);
		color: var(--color-accent);
	}
	a:hover b {
		text-decoration: underline;
		text-decoration-color: var(--color-accent);
	}
	span {
		color: var(--color-ink-muted);
		align-self: center;
	}
	@media (max-width: 560px) {
		a {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
