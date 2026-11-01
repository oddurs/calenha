<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import Interlinear from '$components/language/Interlinear.svelte';
	import Line from '$components/language/Line.svelte';
	import ChipGroup from '$components/ui/ChipGroup.svelte';
	import { textHref } from '$lib/links';

	let { data } = $props();
	const t = $derived(data.text);

	type Mode = 'translation' | 'interlinear' | 'calenha';
	let mode = $state<Mode>('translation');
	const modes: { value: Mode; label: string }[] = [
		{ value: 'translation', label: 'with translation' },
		{ value: 'interlinear', label: 'word by word' },
		{ value: 'calenha', label: 'Calenha only' }
	];

	// an empty line is a stanza break
	const stanzas = $derived(
		t.lines.reduce<(typeof t.lines)[]>(
			(all, line) => {
				if (line.text.trim()) all.at(-1)?.push(line);
				else if (all.at(-1)?.length) all.push([]);
				return all;
			},
			[[]]
		)
	);
</script>

<Meta title={t.title} description="{t.english}: a {t.kind} in Calenha." />

<article class="reading {t.kind}">
	<header class="head">
		<h1 lang="x-calenha">{t.title}</h1>
		<p class="english">{t.english} <span class="kind">{t.kind}</span></p>
	</header>

	<ChipGroup label="How to read" options={modes} bind:value={mode} />

	<div class="lines">
		{#each stanzas as stanza, s (s)}
			{#if stanza.length}
				<div class="stanza">
					{#each stanza as line, i (i)}
						<div class="line">
							{#if mode === 'interlinear'}
								<Interlinear text={line.text} />
							{:else}
								<p class="cal"><Line text={line.text} /></p>
							{/if}
							{#if mode !== 'calenha'}<p class="translation">{line.translation}</p>{/if}
						</div>
					{/each}
				</div>
			{/if}
		{/each}
	</div>

	<aside class="about">
		<h2>about this {t.kind}</h2>
		<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted: from the repo's own data -->
		<p>{@html t.note}</p>
		{#if data.others.length}
			<p>
				Also read
				{#each data.others as other, i (other.slug)}{#if i}{' and '}{/if}<a
						href={textHref(other.slug)}
						lang="x-calenha">{other.title}</a
					>{/each}.
			</p>
		{/if}
	</aside>
</article>

<style>
	.reading {
		display: grid;
		gap: var(--space-m);
	}
	.head {
		display: grid;
		gap: var(--space-2xs);
		padding-top: var(--space-xl);
	}
	h1 {
		font-size: var(--step-6);
		line-height: 1.1;
	}
	.english {
		font-size: var(--step-2);
	}
	.kind {
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step-0);
	}
	.lines {
		display: grid;
		gap: var(--space-l);
		padding-top: var(--space-xs);
	}
	.stanza {
		display: grid;
		gap: var(--space-s);
	}
	.line {
		display: grid;
		gap: var(--space-3xs);
	}
	.cal {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
	}
	.story .cal {
		font-size: var(--step-1);
	}
	.translation {
		font-style: italic;
		color: var(--color-ink-muted);
	}
	.about {
		padding-top: var(--space-xl);
		display: grid;
		gap: var(--space-xs);
		max-width: 40em;
	}
	.about h2 {
		font-size: var(--step-1);
		color: var(--color-accent);
	}
</style>
