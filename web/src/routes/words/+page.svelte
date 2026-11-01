<script lang="ts">
	import { resolve } from '$app/paths';
	import Meta from '$components/layout/Meta.svelte';
	import EntryRow from '$components/language/EntryRow.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import SearchField from '$components/ui/SearchField.svelte';
	import Tabs from '$components/ui/Tabs.svelte';
	import { language, plain } from '$lib/language';

	let query = $state('');
	let domain = $state('');

	const domains = [
		{ value: '', label: 'every domain' },
		...language.domains.map((d) => ({ value: d.name, label: d.name, title: d.intro }))
	];

	// searched against the word (with and without accents), its gloss and its sense
	const haystack = new Map(
		language.entries.map((e) => [e.slug, plain([e.word, e.gloss, e.sense ?? ''].join(' '))])
	);

	const shown = $derived.by(() => {
		const term = plain(query);
		return language.entries.filter(
			(e) => (!domain || e.domain === domain) && (!term || haystack.get(e.slug)?.includes(term))
		);
	});

	const letters = $derived.by(() => {
		const groups: { letter: string; entries: typeof shown }[] = [];
		for (const e of shown) {
			const letter = plain(e.word).charAt(0);
			const last = groups.at(-1);
			if (last?.letter === letter) last.entries.push(e);
			else groups.push({ letter, entries: [e] });
		}
		return groups;
	});
</script>

<Meta title="words" description="The Calenha dictionary: {language.meta.counts.words} words." />

<PageHeader
	english="words"
	calenha="palaura"
	lede="Every word of the calm speech, from the sea inward, the way the fog travels."
/>

<div class="find margined">
	<p class="margin count" aria-live="polite">
		{shown.length}
		{shown.length === 1 ? 'word' : 'words'}
	</p>
	<div class="main tools">
		<SearchField
			id="q"
			label="Find a word in Calenha or English"
			placeholder="river, mirão, light"
			bind:value={query}
		/>
		<Tabs label="Domain" options={domains} bind:value={domain} size="small" />
	</div>
</div>

{#if shown.length === 0}
	<div class="margined">
		<p class="main empty">
			No word for that yet. Try it in English or in Calenha, or look among the
			<a href={resolve('/unspoken')}>unspoken words</a>, which are waiting for meanings.
		</p>
	</div>
{/if}

{#each letters as group (group.letter)}
	<section class="letter margined" aria-label="Words beginning with {group.letter}">
		<h2 class="margin" lang="x-calenha">{group.letter}</h2>
		<div class="main">
			{#each group.entries as e (e.slug)}
				<EntryRow entry={e} />
			{/each}
		</div>
	</section>
{/each}

<style>
	.find {
		padding-bottom: var(--space-l);
		align-items: end;
	}
	.tools {
		display: grid;
		gap: var(--space-s);
	}
	.count {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		padding-bottom: 0.6rem;
	}
	.empty {
		padding-block: var(--space-l);
		max-width: var(--text-max);
	}
	.letter {
		padding-top: var(--space-s);
	}
	.letter h2 {
		font-size: var(--step-5);
		line-height: 1;
		color: var(--color-accent);
		align-self: start;
		padding-top: var(--space-m);
	}
	@media (min-width: 761px) {
		.letter h2 {
			position: sticky;
			top: var(--space-m);
		}
	}
	@media (max-width: 760px) {
		.count {
			order: 2;
			padding-bottom: 0;
		}
		.letter h2 {
			font-size: var(--step-3);
			padding-top: var(--space-l);
		}
	}
</style>
