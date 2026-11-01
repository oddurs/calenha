<script lang="ts">
	import { onMount } from 'svelte';
	import Horizon from '$components/layout/Horizon.svelte';
	import Meta from '$components/layout/Meta.svelte';
	import Line from '$components/language/Line.svelte';
	import Word from '$components/language/Word.svelte';
	import Section from '$components/ui/Section.svelte';
	import { HOURS, hourInfo } from '$design/hours';
	import { featured, language, lookup } from '$lib/language';
	import { textHref, wordHref } from '$lib/links';
	import { href } from '$lib/sections';

	const things = [
		{
			title: 'every verb is an invitation',
			line: 'nã velu · calu.',
			text: 'Verbs end in -u, and there is no way to give a command. This says “there’s no need to wander; rest.”'
		},
		{
			title: 'time is a tide',
			line: 'vaza nevoã · chea solouro.',
			text: 'Vaza, the ebb, marks what has passed; chea, the flood, what is coming. “The fog has gone out; the golden hour is coming in.”'
		},
		{
			title: 'a space can be a silence',
			line: 'aswen tu velu · solenha.',
			text: 'The breath mark is a pause, said aloud, that closes a condition the way a block of code ends. “If you wander, there will be light through the leaves.”'
		},
		{
			title: 'capitals are a bow',
			line: 'lë Miraluma miru.',
			text: 'Everything is written in lowercase, so a capital letter is reverence. “The redwood remembers.”'
		},
		{
			title: 'words grow from roots',
			line: 'thal · thalírë · thalu',
			text: 'From thal, flow: thalírë, the ever-flowing, which is a river; and thalu, to flow.'
		}
	];

	// a word for the tide: the same all day, a different one tomorrow
	const candidates = language.entries.filter(
		(e) => e.sense && (e.pos === 'noun' || e.pos === 'verb') && e.syllables.length > 1
	);
	let tideWord = $state(lookup('saudadë') ?? candidates[0]);
	onMount(() => {
		const day = Math.floor(Date.now() / 86_400_000);
		tideWord = candidates[day % candidates.length] ?? tideWord;
	});

	const poem = language.texts.find((t) => t.slug === 'nevoa');
	const poemLine = poem?.lines.find((l) => l.text.includes('venida'));
	const places = ['algamar', 'miraluma', 'ouressa', 'pedralta', 'lonjura']
		.map((w) => lookup(w))
		.filter((e) => e !== undefined);
</script>

<Meta
	description="Calenha, the calm speech: a constructed language for a California that was never hurried."
/>

<Horizon>
	{#snippet sky()}
		<p class="opening"><Line text={featured.text} links={false} breathe /></p>
	{/snippet}
	{#snippet sea()}
		<p class="translation">{featured.translation}</p>
		<p class="hour-note">
			In Solmara it is
			{#each HOURS as h (h)}<span class="when" data-for={h}
					><span lang="x-calenha">{hourInfo[h].word}</span>, {hourInfo[h].english}</span
				>{/each}. The page is coloured for the hour.
		</p>
	{/snippet}
</Horizon>

<div class="frame">
	<Section id="calm" title="the calm speech">
		<p class="intro">
			Calenha is spoken by the Calenhi of Solmara, a California one step to the side of ours, where
			the coast was never paved and nothing was ever hurried. It sounds like Portuguese with a touch
			of English, it is written mostly in lowercase, and it takes its silences seriously.
		</p>
		<p class="hint">
			Hover over a word in any line to see what it means and where its stress falls. Every word
			leads to a page of its own.
		</p>
	</Section>

	<Section id="five" title="five things to know">
		<ul class="things">
			{#each things as thing (thing.title)}
				<li>
					<p class="example"><Line text={thing.line} /></p>
					<h3>{thing.title}</h3>
					<p class="explain">{thing.text}</p>
				</li>
			{/each}
		</ul>
	</Section>

	<Section id="begin" title="where to begin">
		<div class="doors">
			<a class="door" href={href('/words')}>
				<span class="cal" lang="x-calenha">palaura</span>
				<span class="en">the dictionary</span>
				<span class="sample">
					{language.meta.counts.words} words, grown from {language.meta.counts.roots} roots.
				</span>
			</a>
			{#if tideWord}
				<a class="door tide" href={wordHref(tideWord.slug)}>
					<span class="label">a word for today</span>
					<span class="big"><Word shape={tideWord} /></span>
					<span class="sample"
						><b>{tideWord.gloss}</b>{tideWord.sense ? `. ${tideWord.sense}` : ''}</span
					>
				</a>
			{/if}
			<a class="door" href={href('/grammar')}>
				<span class="cal" lang="x-calenha">como</span>
				<span class="en">how the language works</span>
				<span class="sample">
					Invitations, tide-time, the breath, the bow, and the sounds that hold them.
				</span>
			</a>
			{#if poem && poemLine}
				<a class="door" href={textHref(poem.slug)}>
					<span class="cal" lang="x-calenha">lenda</span>
					<span class="en">texts to read</span>
					<span class="sample"
						><span class="quote" lang="x-calenha">{poemLine.text}</span>
						{poemLine.translation}</span
					>
				</a>
			{/if}
			<a class="door wide" href={href('/world')}>
				<span class="cal" lang="x-calenha">solmara</span>
				<span class="en">the land and its people</span>
				<span class="places">
					{#each places as p (p.slug)}<span
							><span lang="x-calenha">{p.word}</span> <i>{p.short}</i></span
						>{/each}
				</span>
			</a>
		</div>
	</Section>
</div>

<style>
	.opening {
		font-size: var(--step-5);
		line-height: 1.08;
		letter-spacing: -0.012em;
		max-width: 15em;
		text-wrap: balance;
	}
	.translation {
		font-size: var(--step-2);
		line-height: var(--leading-snug);
		font-style: italic;
	}
	.hour-note {
		padding-top: var(--space-s);
		font-size: var(--step--1);
		opacity: 0.85;
	}
	.hour-note [lang] {
		font-size: 1.15em;
	}
	.when {
		display: none;
	}
	/* the hour is set on <html> before first paint, so the note never flickers */
	:global(html:not([data-hour])) .when[data-for='nevoa'],
	:global(html[data-hour='alva']) .when[data-for='alva'],
	:global(html[data-hour='nevoa']) .when[data-for='nevoa'],
	:global(html[data-hour='tarde']) .when[data-for='tarde'],
	:global(html[data-hour='solouro']) .when[data-for='solouro'],
	:global(html[data-hour='noite']) .when[data-for='noite'] {
		display: inline;
	}

	.intro {
		font-size: var(--step-1);
		line-height: 1.45;
		max-width: 32em;
	}
	.hint {
		color: var(--color-ink-muted);
		max-width: var(--text-max);
	}

	.things {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-l);
	}
	.things li {
		display: grid;
		gap: var(--space-3xs);
		max-width: 36rem;
	}
	.example {
		font-size: var(--step-3);
		line-height: var(--leading-tight);
		padding-bottom: var(--space-2xs);
	}
	.things h3 {
		font-size: var(--step-0);
		font-weight: 700;
	}
	.explain {
		color: var(--color-ink-muted);
	}

	.doors {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		border-top: var(--rule);
	}
	.door {
		display: grid;
		align-content: start;
		gap: var(--space-3xs);
		padding: var(--space-m) var(--space-m) var(--space-l) 0;
		border-bottom: var(--rule);
		text-decoration: none;
		transition: background-color var(--duration-quick) var(--ease-tide);
	}
	.door:nth-child(even) {
		padding-left: var(--space-m);
		border-left: var(--rule);
	}
	.door.wide {
		grid-column: 1 / -1;
		padding-left: 0;
		border-left: 0;
	}
	.door:hover .cal,
	.door:hover .big {
		color: var(--color-accent);
	}
	.cal {
		font-size: var(--step-4);
		line-height: var(--leading-display);
		transition: color var(--duration-quick) var(--ease-tide);
	}
	.en {
		font-weight: 500;
		padding-bottom: var(--space-2xs);
	}
	.sample {
		color: var(--color-ink-muted);
		max-width: 26em;
	}
	.sample b {
		color: var(--color-ink);
		font-weight: 500;
	}
	.quote {
		display: block;
		color: var(--color-ink);
		font-size: var(--step-1);
		padding-bottom: var(--space-3xs);
	}
	.label {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.big {
		font-size: var(--step-4);
		line-height: var(--leading-display);
		padding-block: var(--space-xs) var(--space-3xs);
		transition: color var(--duration-quick) var(--ease-tide);
	}
	.places {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-l);
		padding-top: var(--space-2xs);
	}
	.places [lang] {
		font-size: var(--step-1);
	}
	.places i {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	@media (max-width: 640px) {
		.doors {
			grid-template-columns: minmax(0, 1fr);
		}
		.door:nth-child(even) {
			padding-left: 0;
			border-left: 0;
		}
	}
</style>
