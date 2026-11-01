<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import Interlinear from '$components/language/Interlinear.svelte';
	import Chip from '$components/ui/Chip.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import SearchField from '$components/ui/SearchField.svelte';
	import { featured, read } from '$lib/language';

	const tries = [
		{ value: 'aswen tu velu · solenha.', label: 'if you wander' },
		{ value: 'lë Miraluma miru.', label: 'the redwood' },
		{ value: 'venha, venida · acá lar.', label: 'for a guest' },
		{ value: 'sera porcë? · porcë Mar lenta.', label: 'why?' }
	];

	let line = $state(featured.text);

	const words = $derived(read(line).filter((t) => t.kind === 'word'));
	const known = $derived(words.filter((t) => t.kind === 'word' && t.entry).length);
</script>

<Meta title="reader" description="Read any line of Calenha, word by word." />

<PageHeader
	title="reader"
	lede="Type a line of Calenha. Each word is read back with its stress and meaning."
/>

<div class="tool">
	<SearchField id="line" label="A line of Calenha" multiline bind:value={line} />
	<div class="tries" role="group" aria-label="Try a line">
		{#each tries as t (t.value)}
			<Chip pressed={line === t.value} onclick={() => (line = t.value)}>{t.label}</Chip>
		{/each}
	</div>
	<p class="count" aria-live="polite">
		{#if words.length}{known} of {words.length} {words.length === 1 ? 'word' : 'words'} known{/if}
	</p>
</div>

<div class="out"><Interlinear text={line} size="large" /></div>

<p class="note">
	The breath mark is typed as a middle dot: <code>·</code>. Words the dictionary does not know yet
	are shown faintly.
</p>

<style>
	.tool {
		display: grid;
		gap: var(--space-s);
	}
	.tries {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs);
	}
	.count {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		min-height: 1.6em;
	}
	.out {
		min-height: 4rem;
		padding-block: var(--space-m);
	}
	.note {
		max-width: var(--measure-text);
	}
</style>
