<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import PhraseList from '$components/language/PhraseList.svelte';
	import Word from '$components/language/Word.svelte';
	import WordList from '$components/language/WordList.svelte';
	import Facts from '$components/ui/Facts.svelte';
	import { language, text } from '$lib/language';
	import { changeHref, rootHref, textHref, wordHref } from '$lib/links';

	let { data } = $props();
	const e = $derived(data.entry);

	const said = $derived(
		e.syllables
			.map((s, i) => (i === e.stress && e.syllables.length > 1 ? s.toUpperCase() : s))
			.join('·')
	);
	const phrases = $derived(
		e.phrases.map((i) => language.phrases[i]).filter((p) => p !== undefined)
	);
	const texts = $derived(e.texts.map(text).filter((t) => t !== undefined));

	const facts = $derived(
		[
			e.parts.length ? { label: 'made from', body: parts } : null,
			e.old ? { label: 'history', body: history } : null,
			e.family.length ? { label: 'family', body: family } : null,
			phrases.length ? { label: 'in use', body: inUse } : null,
			texts.length ? { label: 'in texts', body: inTexts } : null
		].filter((f) => f !== null)
	);
</script>

<Meta title={e.word} description="{e.word}: {e.gloss}. A word of Calenha." />

{#snippet parts()}
	<p class="parts">
		{#each e.parts as part, i (i)}
			{#if i}<span class="plus">+</span>{/if}
			<span class="part">
				{#if part.kind === 'root' && part.target}
					<a href={rootHref(part.target)} lang="x-calenha">{part.form}</a>
				{:else if part.kind === 'word' && part.target}
					<a href={wordHref(part.target)} lang="x-calenha">{part.form}</a>
				{:else}
					<span lang="x-calenha">{part.form}</span>
				{/if}
				<i>{part.meaning}</i>
			</span>
		{/each}
	</p>
{/snippet}

{#snippet history()}
	<p class="chain">
		<span class="old" lang="x-calenha">*{e.old}</span>
		{#each e.history as step (step.index)}
			<span class="to" aria-hidden="true">→</span>
			<span class="step">
				<span lang="x-calenha">{step.form}</span>
				<a href={changeHref(step.index)}>{step.change}</a>
			</span>
		{/each}
	</p>
{/snippet}

{#snippet family()}
	<WordList slugs={e.family} />
{/snippet}

{#snippet inUse()}
	<PhraseList {phrases} />
{/snippet}

{#snippet inTexts()}
	<ul class="texts">
		{#each texts as t (t.slug)}
			<li><a href={textHref(t.slug)} lang="x-calenha">{t.title}</a> <i>{t.english}</i></li>
		{/each}
	</ul>
{/snippet}

<article>
	<header class="word-head">
		<h1><Word shape={e} /></h1>
		<p class="say">
			<span class="syllables" lang="x-calenha">{said}</span>
			<span class="ipa">/{e.ipa}/</span>
		</p>
		<p class="meaning">{e.gloss} <span class="pos">{e.label}</span></p>
		{#if e.sense}<p class="sense">{e.sense}</p>{/if}
	</header>

	<Facts {facts} />

	<nav class="pager" aria-label="Neighbouring words">
		{#if data.before}
			<a href={wordHref(data.before.slug)} rel="prev">← {data.before.word}</a>
		{:else}<span></span>{/if}
		{#if data.after}
			<a href={wordHref(data.after.slug)} rel="next">{data.after.word} →</a>
		{/if}
	</nav>
</article>

<style>
	.word-head {
		display: grid;
		gap: var(--space-2xs);
		padding-block: var(--space-xl) var(--space-xs);
	}
	h1 {
		font-size: var(--step-6);
		line-height: 1.1;
		letter-spacing: -0.015em;
		--stress-offset: 0.1em;
	}
	.say {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3xs) var(--space-m);
		align-items: baseline;
	}
	.syllables {
		font-size: var(--step-1);
		letter-spacing: 0.04em;
	}
	.ipa {
		color: var(--color-accent);
		font-size: var(--step-0);
	}
	.meaning {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
		padding-top: var(--space-xs);
	}
	.pos {
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step-0);
	}
	.sense {
		font-style: italic;
		font-size: var(--step-1);
		max-width: 32em;
	}
	.parts {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-s);
		align-items: baseline;
	}
	.part {
		display: inline-grid;
		font-size: var(--step-1);
	}
	.part i {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.plus,
	.to {
		color: var(--color-ink-muted);
	}
	.chain {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3xs) var(--space-xs);
		align-items: baseline;
	}
	.old {
		color: var(--color-ink-muted);
		font-size: var(--step-1);
	}
	.step {
		display: inline-grid;
		font-size: var(--step-1);
	}
	.step a {
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}
	.texts {
		list-style: none;
		padding: 0;
	}
	.texts i {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.pager {
		display: flex;
		justify-content: space-between;
		gap: var(--space-m);
		padding-top: var(--space-l);
	}
	.pager a {
		text-decoration: none;
		color: var(--color-ink-muted);
	}
	.pager a:hover {
		color: var(--color-ink);
	}
</style>
