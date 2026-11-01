<script lang="ts">
	import { resolve } from '$app/paths';
	import Meta from '$components/layout/Meta.svelte';
	import Line from '$components/language/Line.svelte';
	import PhraseList from '$components/language/PhraseList.svelte';
	import LinkList from '$components/ui/LinkList.svelte';
	import Section from '$components/ui/Section.svelte';
	import { featured, language } from '$lib/language';

	const counts = language.meta.counts;

	const things = [
		{
			title: 'every verb is an invitation',
			line: 'nã velu · calu.',
			text: 'Verbs end in -u, and there is no way to command. This line means “there’s no need to wander; rest.”'
		},
		{
			title: 'time is a tide',
			line: 'vaza nevoã · chea solouro.',
			text: 'Vaza (ebb) marks what has passed, chea (flood) what is coming. “The fog has gone out; the golden hour is coming in.”'
		},
		{
			title: 'a space can be a silence',
			line: 'aswen tu velu · solenha.',
			text: 'The breath mark is a pause that closes a condition, the way a block ends. “If you wander, there will be light through the leaves.”'
		},
		{
			title: 'capitals are a bow',
			line: 'lë Miraluma miru.',
			text: 'Everything is lowercase, so a capital is reverence. “The redwood remembers.”'
		},
		{
			title: 'words grow from roots',
			line: 'thalírë · altavel',
			text: 'Thal (flow) and -írë (the ever-) make the river. Alt (high) and vel (wander) make the condor, the high wanderer.'
		}
	];

	const ways = [
		{
			label: 'words',
			href: resolve('/words'),
			note: `all ${counts.words} words, in Calenha or English`
		},
		{
			label: 'roots',
			href: resolve('/roots'),
			note: `the ${counts.roots} roots and the endings words grow from`
		},
		{
			label: 'grammar',
			href: resolve('/grammar'),
			note: 'invitation, tide-time, the breath, the bow'
		},
		{ label: 'sounds', href: resolve('/sounds'), note: 'vowels, consonants, syllables and stress' },
		{
			label: 'phrases',
			href: resolve('/phrases'),
			note: `${counts.phrases} things to say, from greetings to sayings`
		},
		{
			label: 'texts',
			href: resolve('/texts'),
			note: 'a poem, a story and a blessing, word by word'
		},
		{ label: 'reader', href: resolve('/reader'), note: 'type a line of Calenha and read it' },
		{
			label: 'history',
			href: resolve('/history'),
			note: 'how Old Calenha softened into the modern tongue'
		},
		{ label: 'world', href: resolve('/world'), note: 'Solmara and the Calenhi' }
	];

	// the first two phrases of each topic
	const sample = language.topics.flatMap((topic) =>
		language.phrases.filter((p) => p.topic === topic && !p.featured).slice(0, 2)
	);
</script>

<Meta description="Calenha, the calm speech: a constructed language for a mythical California." />

<header class="hero">
	<p class="opening"><Line text={featured.text} links={false} breathe /></p>
	<p class="translation">{featured.translation}</p>
	<div class="intro">
		<p>
			Calenha is the calm speech of the Calenhi of Solmara, a California one step to the side of
			ours, where nothing was ever hurried. It sounds like Portuguese with a touch of English, and
			it takes its silences seriously.
		</p>
		<p>
			Gold marks the syllable that carries the stress. Tap any word in an example to visit its own
			page.
		</p>
	</div>
</header>

<Section id="five" title="five things to know">
	<ul class="things">
		{#each things as thing (thing.title)}
			<li>
				<h3>{thing.title}</h3>
				<p class="example"><Line text={thing.line} /></p>
				<p>{thing.text}</p>
			</li>
		{/each}
	</ul>
</Section>

<Section id="begin" title="where to begin">
	<LinkList items={ways} />
</Section>

<Section id="use" title="in use">
	<PhraseList phrases={sample} />
	<p><a href={resolve('/phrases')}>all {counts.phrases} phrases</a></p>
</Section>

<style>
	.hero {
		padding-block: clamp(2rem, 7vw, 5rem) var(--space-m);
		display: grid;
		gap: var(--space-m);
	}
	.opening {
		font-size: var(--step-5);
		line-height: 1.12;
		letter-spacing: -0.01em;
		text-wrap: balance;
		--stress-offset: 0.1em;
	}
	.translation {
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step-1);
	}
	.intro {
		max-width: var(--measure-text);
		display: grid;
		gap: var(--space-xs);
	}
	.things {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-m);
	}
	.things li {
		display: grid;
		gap: var(--space-3xs);
		max-width: 36em;
	}
	.things h3 {
		font-size: var(--step-1);
	}
	.example {
		font-size: var(--step-1);
		color: var(--color-accent);
	}
</style>
