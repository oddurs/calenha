<!--
  @component
  One word in the dictionary: the headword with its beat, and everything known about it.
-->
<script lang="ts">
	import type { Entry } from '$lib/language';
	import { rootHref, wordHref } from '$lib/links';
	import Word from './Word.svelte';

	let { entry }: { entry: Entry } = $props();
</script>

<article class="entry">
	<h3 class="headword"><Word shape={entry} href={wordHref(entry.slug)} /></h3>
	<div class="body">
		<p class="gloss">{entry.gloss}<span class="pos">{entry.label}</span></p>
		<p class="ipa">/{entry.ipa}/</p>
		{#if entry.sense}<p class="sense">{entry.sense}</p>{/if}
		{#if entry.parts.length || entry.old}
			<p class="ety">
				{#each entry.parts as part, i (i)}{#if i}<span class="plus">
							+
						</span>{/if}{#if part.kind === 'root' && part.target}<a
							href={rootHref(part.target)}
							lang="x-calenha">{part.form}</a
						>{:else if part.kind === 'word' && part.target}<a
							href={wordHref(part.target)}
							lang="x-calenha">{part.form}</a
						>{:else}<span lang="x-calenha">{part.form}</span>{/if}{/each}{#if entry.old}<span
						class="old"
						>{entry.parts.length ? ', from older ' : 'from older '}<span lang="x-calenha"
							>*{entry.old}</span
						></span
					>{/if}
			</p>
		{/if}
	</div>
</article>

<style>
	.entry {
		display: grid;
		grid-template-columns: minmax(0, 13rem) minmax(0, 1fr);
		gap: var(--space-3xs) var(--space-l);
		padding-block: var(--space-m);
		border-top: var(--rule);
	}
	.headword {
		font-size: var(--step-3);
		line-height: var(--leading-tight);
		padding-top: 0.15rem;
	}
	.body {
		min-width: 0;
		display: grid;
		gap: 0.1rem;
		align-content: start;
	}
	.gloss {
		font-size: var(--step-1);
		font-weight: 500;
		line-height: var(--leading-snug);
	}
	.pos {
		font-weight: 400;
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		margin-left: 0.6em;
	}
	.ipa {
		color: var(--color-accent);
	}
	.sense {
		font-style: italic;
		max-width: 34em;
		padding-top: var(--space-3xs);
	}
	.ety {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		padding-top: var(--space-3xs);
	}
	.ety a {
		color: var(--color-ink);
		font-size: 1.1em;
	}
	.plus {
		color: var(--color-ink-muted);
	}
	@media (max-width: 560px) {
		.entry {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
