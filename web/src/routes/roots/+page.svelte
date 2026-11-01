<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import WordList from '$components/language/WordList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import Section from '$components/ui/Section.svelte';
	import { language } from '$lib/language';
</script>

<Meta title="roots" description="The roots and endings of Calenha." />

<PageHeader
	title="roots"
	lede="The seeds words grow from. A root is never said alone; it waits for an ending."
/>

<ul class="roots">
	{#each language.roots as r (r.slug)}
		<li id="r-{r.slug}">
			<p class="root" lang="x-calenha">{r.root}</p>
			<div class="about">
				<p class="meaning">{r.meaning}</p>
				{#if r.kin}<p class="kin">{r.kin}</p>{/if}
				<WordList slugs={r.children} gloss={false} />
			</div>
		</li>
	{/each}
</ul>

<Section id="endings" title="endings">
	<p class="note">
		Endings turn roots into words. When an ending that begins with a vowel meets a word that ends in
		one, the first vowel gives way: calenha and -i make calenhi.
	</p>
	<div class="table">
		<table>
			<thead><tr><th>ending</th><th>adds</th><th>as in</th></tr></thead>
			<tbody>
				{#each language.affixes as a (a.form + a.makes)}
					<tr>
						<td lang="x-calenha" class="form">{a.form}</td>
						<td>{a.meaning}</td>
						<td><WordList slugs={a.examples} gloss={false} /></td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</Section>

<style>
	.roots {
		list-style: none;
		padding: 0;
		border-top: var(--rule);
	}
	.roots li {
		display: grid;
		grid-template-columns: minmax(0, 7rem) minmax(0, 1fr);
		gap: var(--space-3xs) var(--space-m);
		padding-block: var(--space-s);
		border-bottom: var(--rule);
		scroll-margin-top: var(--space-m);
	}
	.root {
		font-size: var(--step-2);
		color: var(--color-accent);
		line-height: var(--leading-snug);
	}
	.about {
		min-width: 0;
		display: grid;
		gap: var(--space-3xs);
	}
	.kin {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		font-style: italic;
	}
	.note {
		max-width: var(--measure-text);
	}
	.table {
		overflow-x: auto;
	}
	table {
		border-collapse: collapse;
		width: 100%;
		font-size: var(--step--1);
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
		vertical-align: top;
	}
	.form {
		font-size: var(--step-1);
		white-space: nowrap;
	}
	@media (max-width: 560px) {
		.roots li {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
