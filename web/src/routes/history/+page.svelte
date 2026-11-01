<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import WordList from '$components/language/WordList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import Section from '$components/ui/Section.svelte';
	import { language } from '$lib/language';
	import { wordHref } from '$lib/links';

	const old = language.entries.filter((e) => e.old);
</script>

<Meta title="history" description="How Old Calenha softened into the modern language." />

<PageHeader
	title="history"
	lede="Old Calenha was harder: k, doubled vowels, plain endings. Over many generations the sea air wore it smooth."
/>

<p class="note">
	These are the changes, in the order they happened. Order matters: the long vowels formed before n
	and l softened, which is why *thaliire became thalírë and not thalhirë.
</p>

<ol class="changes">
	{#each language.changes as c (c.index)}
		<li id="c-{c.index}">
			<h2>{c.name}</h2>
			<p class="rule" lang="x-calenha">
				{c.rule.map(([a, b]) => `${a} → ${b}`).join(', ')}
				{#if c.environment}<span class="where">{c.environment}</span>{/if}
			</p>
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted: from the repo's own data -->
			<p>{@html c.note}</p>
			{#if c.shaped.length}
				<div class="shaped"><span>shaped</span> <WordList slugs={c.shaped} gloss={false} /></div>
			{/if}
		</li>
	{/each}
</ol>

<Section id="old" title="every old form">
	<div class="table">
		<table>
			<thead><tr><th>old</th><th>now</th><th>meaning</th></tr></thead>
			<tbody>
				{#each old as e (e.slug)}
					<tr>
						<td lang="x-calenha">*{e.old}</td>
						<td><a href={wordHref(e.slug)} lang="x-calenha">{e.word}</a></td>
						<td>{e.gloss}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</Section>

<style>
	.note {
		max-width: 40em;
	}
	.changes {
		list-style: none;
		padding: 0;
		margin-top: var(--space-m);
		border-top: var(--rule);
		counter-reset: change;
	}
	.changes li {
		padding-block: var(--space-m);
		border-bottom: var(--rule);
		display: grid;
		gap: var(--space-2xs);
		scroll-margin-top: var(--space-m);
	}
	h2 {
		font-size: var(--step-1);
	}
	/* the changes are a sequence, so they are numbered */
	h2::before {
		counter-increment: change;
		content: counter(change) '. ';
		color: var(--color-ink-muted);
	}
	.rule {
		font-size: var(--step-1);
		color: var(--color-accent);
	}
	.where {
		color: var(--color-ink-muted);
	}
	.shaped {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3xs) var(--space-xs);
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.table {
		overflow-x: auto;
	}
	table {
		border-collapse: collapse;
		width: 100%;
	}
	th {
		text-align: left;
		font-weight: 400;
		font-style: italic;
		color: var(--color-ink-muted);
	}
	th,
	td {
		padding: 0.45rem 0.9rem 0.45rem 0;
		border-bottom: var(--rule);
	}
</style>
