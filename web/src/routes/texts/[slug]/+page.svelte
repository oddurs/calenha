<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import Interlinear from '$components/language/Interlinear.svelte';
	import Line from '$components/language/Line.svelte';
	import Tabs from '$components/ui/Tabs.svelte';
	import { textHref } from '$lib/links';

	let { data } = $props();
	const t = $derived(data.text);

	type Mode = 'facing' | 'interlinear' | 'calenha';
	let mode = $state<Mode>('facing');
	const modes: { value: Mode; label: string }[] = [
		{ value: 'facing', label: 'facing translation' },
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

<article class="reading {t.kind} mode-{mode}">
	<header class="head margined">
		<p class="margin kind">a {t.kind}</p>
		<div class="main">
			<h1 lang="x-calenha">{t.title}</h1>
			<p class="english">{t.english}</p>
		</div>
	</header>

	<div class="margined controls">
		<p class="margin label">read it</p>
		<div class="main"><Tabs label="How to read" options={modes} bind:value={mode} /></div>
	</div>

	<div class="margined">
		<div class="main lines">
			{#each stanzas as stanza, s (s)}
				{#if stanza.length}
					<div class="stanza">
						{#each stanza as line, i (i)}
							<div class="pair">
								{#if mode === 'interlinear'}
									<div class="cal"><Interlinear text={line.text} /></div>
								{:else}
									<p class="cal"><Line text={line.text} /></p>
								{/if}
								{#if mode !== 'calenha'}<p class="en">{line.translation}</p>{/if}
							</div>
						{/each}
					</div>
				{/if}
			{/each}
		</div>
	</div>

	<aside class="about margined">
		<h2 class="margin">about this {t.kind}</h2>
		<div class="main">
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted: from the repo's own data -->
			<p>{@html t.note}</p>
			{#if data.others.length}
				<p class="more">
					Also read
					{#each data.others as other, i (other.slug)}{#if i}{' and '}{/if}<a
							href={textHref(other.slug)}
							lang="x-calenha">{other.title}</a
						>{/each}.
				</p>
			{/if}
		</div>
	</aside>
</article>

<style>
	.head {
		padding-block: var(--space-xl) var(--space-m);
		align-items: baseline;
	}
	.kind,
	.label {
		color: var(--color-ink-muted);
	}
	h1 {
		font-size: var(--step-6);
		line-height: 1;
		letter-spacing: -0.015em;
	}
	.english {
		font-size: var(--step-2);
		font-weight: 500;
		padding-top: var(--space-2xs);
	}
	.controls {
		padding-bottom: var(--space-l);
		align-items: baseline;
	}
	.lines {
		display: grid;
		gap: var(--space-xl);
	}
	.stanza {
		display: grid;
		gap: var(--space-s);
	}

	/* facing translation: Calenha on the left, English on the right, line by line —
	   the convention of a bilingual edition */
	.pair {
		display: grid;
		gap: var(--space-3xs);
	}
	.mode-facing .pair {
		grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr);
		column-gap: var(--space-l);
		align-items: baseline;
	}
	.cal {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
	}
	.poem .cal,
	.blessing .cal {
		font-size: var(--step-3);
		line-height: 1.2;
	}
	.mode-calenha .cal {
		font-size: var(--step-4);
		line-height: 1.12;
	}
	.mode-interlinear .cal {
		font-size: var(--step-0);
	}
	.en {
		color: var(--color-ink-muted);
	}
	.mode-facing .en {
		font-size: var(--step-1);
		font-style: italic;
	}
	.mode-interlinear .stanza {
		gap: var(--space-l);
	}

	.about {
		margin-top: var(--space-2xl);
		padding-top: var(--space-m);
		border-top: var(--rule);
	}
	.about h2 {
		font-size: var(--step-0);
		font-weight: 500;
	}
	.about .main {
		display: grid;
		gap: var(--space-s);
		max-width: var(--text-max);
	}
	.about :global([lang='x-calenha']) {
		font-size: 1.1em;
	}

	@media (max-width: 760px) {
		.mode-facing .pair {
			grid-template-columns: minmax(0, 1fr);
		}
		.head {
			padding-top: var(--space-l);
		}
	}
</style>
