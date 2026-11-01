<!--
  @component
  A list of places to go: a Calenha name, its English, and a line about it.
-->
<script lang="ts">
	interface Item {
		href: string;
		calenha: string;
		english: string;
		note: string;
	}

	let { items }: { items: Item[] } = $props();
</script>

<ul class="links">
	{#each items as item (item.href)}
		<li>
			<a href={item.href}>
				<span class="cal" lang="x-calenha">{item.calenha}</span>
				<span class="en">{item.english}</span>
				<span class="note">{item.note}</span>
			</a>
		</li>
	{/each}
</ul>

<style>
	.links {
		list-style: none;
		padding: 0;
	}
	li {
		border-top: var(--rule);
	}
	li:last-child {
		border-bottom: var(--rule);
	}
	a {
		display: grid;
		grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
		grid-template-areas: 'cal en' 'cal note';
		gap: 0 var(--space-l);
		padding-block: var(--space-m);
		text-decoration: none;
	}
	.cal {
		grid-area: cal;
		font-size: var(--step-4);
		line-height: var(--leading-display);
	}
	.en {
		grid-area: en;
		font-weight: 500;
		align-self: end;
	}
	.note {
		grid-area: note;
		color: var(--color-ink-muted);
	}
	a:hover .cal {
		color: var(--color-accent);
	}
	@media (max-width: 560px) {
		a {
			grid-template-columns: minmax(0, 1fr);
			grid-template-areas: 'cal' 'en' 'note';
		}
	}
</style>
