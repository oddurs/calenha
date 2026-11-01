<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import EntryRow from '$components/language/EntryRow.svelte';
	import ChipGroup from '$components/ui/ChipGroup.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import SearchField from '$components/ui/SearchField.svelte';
	import { resolve } from '$app/paths';
	import { language, plain } from '$lib/language';

	let query = $state('');
	let domain = $state('');

	const domains = [
		{ value: '', label: 'all' },
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

<PageHeader title="words" lede="From the sea inward, the way the fog travels." />

<div class="find">
	<SearchField
		id="q"
		label="Find a word in Calenha or English"
		placeholder="river, mirão, light…"
		bind:value={query}
	/>
	<ChipGroup label="Filter by domain" options={domains} bind:value={domain} />
	<p class="count" aria-live="polite">{shown.length} {shown.length === 1 ? 'word' : 'words'}</p>
</div>

{#if shown.length === 0}
	<p class="empty">
		No word for that yet. Try it in English or in Calenha, or see the
		<a href={resolve('/unspoken')}>unspoken words</a> waiting for a meaning.
	</p>
{/if}

{#each letters as group (group.letter)}
	<section class="letter" aria-label={group.letter}>
		<h2>{group.letter}</h2>
		{#each group.entries as e (e.slug)}
			<EntryRow entry={e} />
		{/each}
	</section>
{/each}

<style>
	.find {
		display: grid;
		gap: var(--space-s);
	}
	.count {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.empty {
		padding-block: var(--space-m);
		max-width: var(--measure-text);
	}
	.letter h2 {
		font-size: var(--step-4);
		color: var(--color-accent);
		line-height: 1;
		padding-block: var(--space-l) var(--space-2xs);
	}
</style>
