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

	const phrases = $derived(
		e.phrases.map((i) => language.phrases[i]).filter((p) => p !== undefined)
	);
	const texts = $derived(e.texts.map(text).filter((t) => t !== undefined));

	const facts = $derived(
		[
			e.parts.length ? { label: 'made from', body: parts } : null,
			e.old ? { label: 'how it came to be', body: history } : null,
			e.family.length ? { label: 'its family', body: family } : null,
			phrases.length ? { label: 'in use', body: inUse } : null,
			texts.length ? { label: 'in texts', body: inTexts } : null
		].filter((f) => f !== null)
	);
</script>

<Meta title={e.word} description="{e.word}: {e.gloss}. A word of Calenha." />

{#snippet parts()}
	<p class="parts">
		{#each e.parts as part, i (i)}
			{#if i}<span class="plus" aria-hidden="true">+</span>{/if}
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
	<ol class="chain">
		<li><span class="form old" lang="x-calenha">*{e.old}</span><i>Old Calenha</i></li>
		{#each e.history as step (step.index)}
			<li>
				<span class="form" lang="x-calenha">{step.form}</span>
				<a href={changeHref(step.index)}>{step.change}</a>
			</li>
		{/each}
	</ol>
{/snippet}

{#snippet family()}
	<WordList slugs={e.family} />
{/snippet}

{#snippet inUse()}
	<PhraseList {phrases} columns={1} />
{/snippet}

{#snippet inTexts()}
	<ul class="texts">
		{#each texts as t (t.slug)}
			<li><a href={textHref(t.slug)} lang="x-calenha">{t.title}</a> <i>{t.english}</i></li>
		{/each}
	</ul>
{/snippet}

<article>
	<header class="word-head margined">
		<p class="margin pos">{e.label}</p>
		<div class="main">
			<h1><Word shape={e} /></h1>
			<p class="say">
				{#each e.syllables as s, i (i)}{#if i}<span class="dot">·</span>{/if}<span
						lang="x-calenha"
						class:stressed={i === e.stress && e.syllables.length > 1}>{s}</span
					>{/each}
				<span class="ipa">/{e.ipa}/</span>
			</p>
			<p class="meaning">{e.gloss}</p>
			{#if e.sense}<p class="sense">{e.sense}</p>{/if}
		</div>
	</header>

	<Facts {facts} />

	<nav class="pager margined" aria-label="Neighbouring words">
		<div class="main row">
			{#if data.before}
				<a href={wordHref(data.before.slug)} rel="prev"
					><span class="dir" lang="x-calenha">antes</span>
					<span lang="x-calenha">{data.before.word}</span></a
				>
			{:else}<span></span>{/if}
			{#if data.after}
				<a href={wordHref(data.after.slug)} rel="next" class="next"
					><span class="dir" lang="x-calenha">depois</span>
					<span lang="x-calenha">{data.after.word}</span></a
				>
			{/if}
		</div>
	</nav>
</article>

<style>
	.word-head {
		padding-block: var(--space-xl) var(--space-l);
	}
	.pos {
		color: var(--color-ink-muted);
		font-style: italic;
		padding-top: 1.1rem;
	}
	.main {
		display: grid;
		gap: var(--space-2xs);
	}
	h1 {
		font-size: var(--step-6);
		line-height: 1;
		letter-spacing: -0.015em;
		padding-top: 0.12em;
	}
	.say {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0 0.1em;
		font-size: var(--step-1);
		color: var(--color-ink-muted);
	}
	.stressed {
		color: var(--color-ink);
		text-decoration: overline;
		text-decoration-color: var(--color-beat);
		text-decoration-thickness: 2px;
	}
	.dot {
		padding-inline: 0.12em;
	}
	.say .ipa {
		margin-left: var(--space-m);
		color: var(--color-accent);
		font-size: var(--step-0);
	}
	.meaning {
		font-size: var(--step-3);
		line-height: var(--leading-tight);
		font-weight: 500;
		padding-top: var(--space-s);
	}
	.sense {
		font-size: var(--step-1);
		line-height: 1.45;
		font-style: italic;
		max-width: 30em;
		color: var(--color-ink-muted);
	}
	.parts {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-m);
		align-items: baseline;
	}
	.part {
		display: inline-grid;
	}
	.part [lang] {
		font-size: var(--step-2);
		line-height: var(--leading-tight);
	}
	.part i,
	.chain i,
	.texts i {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.plus {
		color: var(--color-ink-muted);
		font-size: var(--step-1);
	}
	.chain {
		list-style: none;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-xs) 0;
	}
	.chain li {
		display: inline-grid;
		padding-right: var(--space-m);
	}
	.chain li + li {
		padding-left: var(--space-m);
		border-left: var(--rule);
	}
	.form {
		font-size: var(--step-2);
		line-height: var(--leading-tight);
	}
	.old {
		color: var(--color-ink-muted);
	}
	.chain a {
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}
	.texts {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-3xs);
	}
	.texts a {
		font-size: var(--step-1);
	}
	.pager {
		padding-top: var(--space-l);
		border-top: var(--rule);
	}
	.row {
		display: flex;
		justify-content: space-between;
		gap: var(--space-m);
	}
	.pager a {
		display: grid;
		text-decoration: none;
		font-size: var(--step-2);
		line-height: var(--leading-tight);
	}
	.pager a:hover [lang]:not(.dir) {
		color: var(--color-accent);
	}
	.next {
		text-align: right;
	}
	.dir {
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}
	@media (max-width: 760px) {
		.word-head {
			padding-top: var(--space-l);
		}
		.pos {
			padding-top: 0;
		}
	}
</style>
