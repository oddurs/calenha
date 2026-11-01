<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import Word from '$components/language/Word.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import Section from '$components/ui/Section.svelte';
	import { language } from '$lib/language';

	const groups = [
		{ id: 'things', title: 'things', words: language.unspoken.things },
		{ id: 'invitations', title: 'invitations', words: language.unspoken.invitations }
	];
</script>

<Meta title="unspoken" description="Unclaimed Calenha words, waiting for a meaning." />

<PageHeader title="unspoken" lede="Words the ear has found that mean nothing yet." />

<p class="note">
	Each of these obeys every rule of the language, and each was chosen by the generator for how it
	sounds. None of them has a meaning. To give one, add it to the lexicon in
	<code>lang/lexicon/</code> and it will appear in the dictionary. More can be found with
	<code>calenha gen</code>.
</p>

{#each groups as g (g.id)}
	<Section id={g.id} title={g.title}>
		<ul class="unspoken">
			{#each g.words as w (w.text)}
				<li>
					<span class="w"><Word shape={w} /></span>
					<span class="ipa">/{w.ipa}/</span>
					{#if w.echoes.length}<span class="echo">near {w.echoes.join(', ')}</span>{/if}
				</li>
			{/each}
		</ul>
	</Section>
{/each}

<style>
	.note {
		max-width: 40em;
	}
	.unspoken {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-m) var(--space-l);
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 13rem), 1fr));
	}
	li {
		display: grid;
	}
	.w {
		font-size: var(--step-2);
	}
	.ipa,
	.echo {
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}
</style>
