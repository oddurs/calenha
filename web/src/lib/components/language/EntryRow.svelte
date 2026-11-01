<!--
  @component
  One word in the dictionary: the headword on the left, everything else on the right.
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
		<p class="gloss">{entry.gloss} <span class="pos">{entry.label}</span></p>
		<p class="ipa">/{entry.ipa}/</p>
		{#if entry.sense}<p class="sense">{entry.sense}</p>{/if}
		{#if entry.parts.length || entry.old}
			<p class="ety">
				{#each entry.parts as part, i (i)}{#if i}{' + '}{/if}{#if part.kind === 'root' && part.target}<a
							href={rootHref(part.target)}
							lang="x-calenha">{part.form}</a
						>{:else if part.kind === 'word' && part.target}<a
							href={wordHref(part.target)}
							lang="x-calenha">{part.form}</a
						>{:else}<span lang="x-calenha">{part.form}</span>{/if}{#if part.meaning}{' '}<i
							>{part.meaning}</i
						>{/if}{/each}{#if entry.parts.length && entry.old}{'; '}{/if}{#if entry.old}from older <span
						lang="x-calenha">*{entry.old}</span
					>{/if}
			</p>
		{/if}
	</div>
</article>

<style>
	.entry {
		display: grid;
		grid-template-columns: minmax(0, 11rem) minmax(0, 1fr);
		gap: var(--space-3xs) var(--space-l);
		padding-block: var(--space-s);
		border-top: var(--rule);
	}
	.headword {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
	}
	.body {
		min-width: 0;
	}
	.pos {
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		margin-left: 0.35em;
	}
	.ipa {
		color: var(--color-accent);
		font-size: var(--step--1);
	}
	.sense {
		font-style: italic;
		margin-top: var(--space-2xs);
	}
	.ety {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		margin-top: var(--space-2xs);
	}
	.ety a,
	.ety span {
		color: var(--color-ink);
	}
	@media (max-width: 560px) {
		.entry {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
