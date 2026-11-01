<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import WordList from '$components/language/WordList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import Section from '$components/ui/Section.svelte';
	import { language } from '$lib/language';
	import { wordHref } from '$lib/links';

	const old = language.entries.filter((e) => e.old);
</script>

<Meta title="history" description="How Old Calenha softened into the modern language." />

<PageHeader
	english="history"
	calenha="vaza"
	lede="Old Calenha was harder: k, doubled vowels, plain endings. Over many generations the sea air wore it smooth."
/>

<div class="margined">
	<p class="main lead">
		These are the changes, in the order they happened, and order matters. The long vowels formed
		before <i>n</i> and <i>l</i> softened, which is why <span lang="x-calenha">*thaliire</span>
		became <span lang="x-calenha">thalírë</span>, and not <span lang="x-calenha">thalhirë</span>.
	</p>
</div>

<ol class="changes">
	{#each language.changes as c (c.index)}
		<li id="c-{c.index}" class="margined">
			<p class="margin n">{c.index}</p>
			<div class="main body">
				<h2>{c.name}</h2>
				<p class="rule">
					<span lang="x-calenha">{c.rule.map(([a, b]) => `${a} → ${b}`).join(', ')}</span>
					{#if c.environment}<span class="where">{c.environment}</span>{/if}
				</p>
				<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted: from the repo's own data -->
				<p class="why">{@html c.note}</p>
				{#if c.shaped.length}
					<div class="shaped">
						<span>it shaped</span><WordList slugs={c.shaped} gloss={false} />
					</div>
				{/if}
			</div>
		</li>
	{/each}
</ol>

<Section id="old" title="every old form">
	<ul class="old">
		{#each old as e (e.slug)}
			<li>
				<span class="then" lang="x-calenha">*{e.old}</span>
				<a class="now" href={wordHref(e.slug)} lang="x-calenha">{e.word}</a>
				<span class="g">{e.short}</span>
			</li>
		{/each}
	</ul>
</Section>

<style>
	.lead {
		max-width: var(--text-max);
		padding-bottom: var(--space-l);
	}
	.lead [lang] {
		font-size: 1.12em;
	}
	.changes {
		list-style: none;
		padding: 0;
	}
	.changes li {
		padding-block: var(--space-m);
		border-top: var(--rule);
		scroll-margin-top: var(--space-m);
	}
	.changes li:target {
		background: linear-gradient(to right, var(--color-surface), transparent);
	}
	/* the changes are a sequence, so they are numbered */
	.n {
		font-family: var(--font-calenha);
		font-size: var(--step-3);
		line-height: 1;
		color: var(--color-ink-muted);
		font-variant-numeric: oldstyle-nums;
	}
	.body {
		display: grid;
		gap: var(--space-3xs);
		max-width: var(--text-max);
	}
	h2 {
		font-size: var(--step-1);
	}
	.rule {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0 var(--space-s);
	}
	.rule [lang] {
		font-size: var(--step-2);
		color: var(--color-accent);
	}
	.where {
		color: var(--color-ink-muted);
	}
	.why :global([lang]) {
		font-size: 1.12em;
	}
	.shaped {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--space-3xs) var(--space-s);
		padding-top: var(--space-2xs);
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.old {
		list-style: none;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 15rem), 1fr));
		gap: var(--space-2xs) var(--space-l);
	}
	.old li {
		display: grid;
		grid-template-columns: auto auto 1fr;
		align-items: baseline;
		gap: 0.6em;
	}
	.then {
		color: var(--color-ink-muted);
	}
	.now {
		font-size: 1.15em;
	}
	.g {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		font-style: italic;
	}
</style>
