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

<PageHeader
	english="unspoken"
	calenha="semë"
	lede="Words the ear has found that mean nothing yet. Seeds."
/>

<div class="margined">
	<p class="main note">
		Each of these obeys every rule of the language, and each was chosen by the word generator for
		how it sounds. None of them has a meaning. To give one, add it to the lexicon in
		<code>lang/lexicon/</code>, and it will grow into the dictionary. More can be found with
		<code>calenha gen</code>.
	</p>
</div>

{#each groups as g (g.id)}
	<Section id={g.id} title={g.title}>
		<ul class="unspoken">
			{#each g.words as w (w.text)}
				<li>
					<span class="w"><Word shape={w} /></span>
					<span class="ipa">/{w.ipa}/</span>
					{#if w.echoes.length}<span class="echo"
							>sounds like <span lang="x-calenha">{w.echoes.join(', ')}</span></span
						>{/if}
				</li>
			{/each}
		</ul>
	</Section>
{/each}

<style>
	.note {
		max-width: var(--text-max);
	}
	.unspoken {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-l) var(--space-l);
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 12rem), 1fr));
	}
	li {
		display: grid;
		gap: 0.1rem;
		align-content: start;
	}
	.w {
		font-size: var(--step-3);
		line-height: 1.2;
	}
	.ipa,
	.echo {
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}
	.ipa {
		font-family: var(--font-ipa);
	}
</style>
