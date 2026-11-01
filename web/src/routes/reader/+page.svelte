<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import Interlinear from '$components/language/Interlinear.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import SearchField from '$components/ui/SearchField.svelte';
	import Tabs from '$components/ui/Tabs.svelte';
	import { featured, read } from '$lib/language';

	const tries = [
		{ value: featured.text, label: 'the afternoon' },
		{ value: 'aswen tu velu · solenha.', label: 'if you wander' },
		{ value: 'lë Miraluma miru.', label: 'the redwood' },
		{ value: 'venha, venida · acá lar.', label: 'for a guest' },
		{ value: 'sera porcë? · porcë Mar lenta.', label: 'why?' }
	];

	let line = $state(featured.text);
	let picked = $state(featured.text);

	const words = $derived(read(line).filter((t) => t.kind === 'word'));
	const known = $derived(words.filter((t) => t.kind === 'word' && t.entry).length);
</script>

<Meta title="reader" description="Read any line of Calenha, word by word." />

<PageHeader
	english="reader"
	calenha="olhu"
	lede="Type a line of Calenha, or choose one. Each word is read back with its beat and its meaning."
/>

<div class="tool margined">
	<p class="margin count" aria-live="polite">
		{#if words.length}{known} of {words.length}
			{words.length === 1 ? 'word' : 'words'} known{/if}
	</p>
	<div class="main fields">
		<SearchField id="line" label="A line of Calenha" multiline lang="x-calenha" bind:value={line} />
		<Tabs
			label="Try a line"
			options={tries}
			bind:value={picked}
			size="small"
			onchange={(v) => (line = v)}
		/>
	</div>
</div>

<div class="margined">
	<div class="main out"><Interlinear text={line} size="large" /></div>
</div>

<div class="margined">
	<p class="main note">
		The breath mark is a middle dot, <code>·</code>. On a Mac it is ⌥⇧9; on a phone, hold the full
		stop. Words the dictionary does not know yet are underlined with a wave.
	</p>
</div>

<style>
	.tool {
		align-items: end;
	}
	.fields {
		display: grid;
		gap: var(--space-s);
	}
	.count {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		padding-bottom: 0.6rem;
	}
	.out {
		padding-block: var(--space-xl);
		min-height: 9rem;
	}
	.note {
		max-width: var(--text-max);
		color: var(--color-ink-muted);
	}
	@media (max-width: 760px) {
		.count {
			order: 2;
		}
	}
</style>
