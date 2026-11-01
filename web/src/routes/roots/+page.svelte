<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import WordList from '$components/language/WordList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import Section from '$components/ui/Section.svelte';
	import { language } from '$lib/language';
</script>

<Meta title="roots" description="The roots and endings of Calenha." />

<PageHeader
	english="roots"
	calenha="raízë"
	lede="The seeds words grow from. A root is never said alone; it waits for an ending."
/>

<ul class="roots">
	{#each language.roots as r (r.slug)}
		<li id="r-{r.slug}" class="margined">
			<p class="margin root" lang="x-calenha">{r.root}</p>
			<div class="main about">
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
		one, the first vowel gives way: <span lang="x-calenha">calenha</span> and
		<span lang="x-calenha">-i</span> make <span lang="x-calenha">calenhi</span>.
	</p>
	<ul class="endings">
		{#each language.affixes as a (a.form + a.makes)}
			<li>
				<p class="form" lang="x-calenha">{a.form}</p>
				<div>
					<p>{a.meaning}</p>
					{#if a.examples.length}<WordList slugs={a.examples} gloss={false} />{/if}
				</div>
			</li>
		{/each}
	</ul>
</Section>

<style>
	.roots {
		list-style: none;
		padding: 0;
	}
	.roots li {
		padding-block: var(--space-m);
		border-top: var(--rule);
		scroll-margin-top: var(--space-m);
		row-gap: var(--space-3xs);
	}
	.roots li:target {
		background: linear-gradient(to right, var(--color-surface), transparent);
	}
	.root {
		font-size: var(--step-3);
		line-height: 1;
		color: var(--color-accent);
	}
	.about {
		display: grid;
		gap: var(--space-3xs);
	}
	.meaning {
		font-size: var(--step-1);
		font-weight: 500;
	}
	.kin {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		font-style: italic;
		padding-bottom: var(--space-2xs);
	}
	.note {
		max-width: var(--text-max);
	}
	.endings {
		list-style: none;
		padding: 0;
	}
	.endings li {
		display: grid;
		grid-template-columns: minmax(0, 6rem) minmax(0, 1fr);
		gap: var(--space-2xs) var(--space-m);
		padding-block: var(--space-s);
		border-top: var(--rule);
	}
	.endings li > div {
		display: grid;
		gap: var(--space-3xs);
	}
	.form {
		font-size: var(--step-2);
		line-height: 1.1;
	}
</style>
