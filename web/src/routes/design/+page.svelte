<script lang="ts">
	import { onMount } from 'svelte';
	import Meta from '$components/layout/Meta.svelte';
	import EntryRow from '$components/language/EntryRow.svelte';
	import Interlinear from '$components/language/Interlinear.svelte';
	import Line from '$components/language/Line.svelte';
	import PhraseList from '$components/language/PhraseList.svelte';
	import Word from '$components/language/Word.svelte';
	import Chip from '$components/ui/Chip.svelte';
	import ChipGroup from '$components/ui/ChipGroup.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import SearchField from '$components/ui/SearchField.svelte';
	import Section from '$components/ui/Section.svelte';
	import { colours, motion, space, typeScale } from '$design/tokens';
	import { language, lookup } from '$lib/language';

	// values live only in tokens.css; read them from the page once it is drawn
	let values = $state<Record<string, string>>({});
	onMount(() => {
		const read = () => {
			const style = getComputedStyle(document.documentElement);
			const all = [...colours.flatMap((g) => g.tokens), ...typeScale, ...space, ...motion];
			values = Object.fromEntries(all.map((t) => [t.name, style.getPropertyValue(t.name).trim()]));
		};
		read();
		const watch = new MutationObserver(read);
		watch.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
		const scheme = matchMedia('(prefers-color-scheme: dark)');
		scheme.addEventListener('change', read);
		return () => {
			watch.disconnect();
			scheme.removeEventListener('change', read);
		};
	});

	const thalire = lookup('thalírë');
	const miraluma = lookup('miraluma');
	let demoQuery = $state('');
	let demoMode = $state('one');
	let demoPressed = $state(true);
	let replay = $state(0);
</script>

<Meta
	title="design system"
	description="The Calenha design system: tokens, type, space, motion and components."
/>

<PageHeader
	title="design system"
	lede="Fog, kelp and one poppy. Everything here is quiet except the stressed syllable."
/>

<div class="intro">
	<p>
		Tokens come in three layers. <b>Primitives</b> are the raw palette and scales, named for things
		in Solmara. <b>Semantic</b> tokens give them roles (page, ink, accent, stress) and are the only
		layer that changes between light and dark. <b>Component</b> tokens record decisions particular to
		one component. Components use only the last two.
	</p>
	<p>
		Values live in <code>src/lib/design/tokens.css</code>; this page reads them live, so it is never
		out of date. Switch the theme in the footer to see the semantic layer change.
	</p>
</div>

<Section id="colour" title="colour">
	{#each colours as group (group.layer)}
		<h3 class="sub">{group.layer}</h3>
		<ul class="swatches" class:compact={group.layer === 'primitive'}>
			{#each group.tokens as token (token.name)}
				<li>
					<span class="swatch" style:background="var({token.name})"></span>
					<code>{token.name}</code>
					<span class="value">{values[token.name] ?? ''}</span>
					{#if token.note}<span class="note">{token.note}</span>{/if}
				</li>
			{/each}
		</ul>
	{/each}
</Section>

<Section id="stress" title="the stress mark">
	<p class="lede">
		The system’s one bright accent. Poppy gold, with a hairline beat beneath, on the syllable that
		carries the stress. It is information, never decoration.
	</p>
	{#if thalire && miraluma}
		<div class="stress-demo">
			<span style:font-size="var(--step-6)"><Word shape={thalire} /></span>
			<span style:font-size="var(--step-4)"><Word shape={miraluma} shown="Miraluma" /></span>
			<span style:font-size="var(--step-1)"><Word shape={thalire} /></span>
		</div>
	{/if}
</Section>

<Section id="type" title="type">
	<p class="lede">
		Gentium Book Plus, one family throughout: made for linguists, so it carries IPA properly. A 1.2
		scale on an 18px base; the display steps grow with the screen.
	</p>
	<ul class="scale">
		{#each typeScale as step (step.name)}
			<li>
				<span class="meta"
					><code>{step.name}</code> <span class="value">{values[step.name] ?? ''}</span>
					{#if step.note}<span class="note">{step.note}</span>{/if}</span
				>
				<span class="specimen" style:font-size="var({step.name})" lang="x-calenha"
					>solenha <i>dappled light</i></span
				>
			</li>
		{/each}
	</ul>
</Section>

<Section id="space" title="space">
	<p class="lede">Siblings are spaced with gap, never margins. One scale for everything.</p>
	<ul class="space">
		{#each space as step (step.name)}
			<li>
				<code>{step.name}</code>
				<span class="bar" style:width="var({step.name})"></span>
				<span class="value">{values[step.name] ?? ''}</span>
			</li>
		{/each}
	</ul>
</Section>

<Section id="motion" title="motion">
	<p class="lede">
		One orchestrated moment: the opening line breathes in, word by word, once. Everything else moves
		only when you do.
	</p>
	<ul class="motion">
		{#each motion as m (m.name)}
			<li>
				<code>{m.name}</code> <span class="value">{values[m.name] ?? ''}</span>
				<span class="note">{m.note}</span>
			</li>
		{/each}
	</ul>
	<div class="breathe-demo">
		{#key replay}
			<p class="breathing"><Line text="onda onda onda" links={false} breathe /></p>
		{/key}
		<Chip onclick={() => replay++}>breathe again</Chip>
	</div>
</Section>

<Section id="components" title="components">
	<div class="specimens">
		<div class="specimen-block">
			<h3 class="sub">Chip, ChipGroup</h3>
			<div class="row">
				<Chip pressed={demoPressed} onclick={() => (demoPressed = !demoPressed)}>a chip</Chip>
				<ChipGroup
					label="Demo"
					options={[
						{ value: 'one', label: 'una' },
						{ value: 'two', label: 'dua' },
						{ value: 'three', label: 'trë' }
					]}
					bind:value={demoMode}
				/>
			</div>
		</div>

		<div class="specimen-block">
			<h3 class="sub">SearchField</h3>
			<SearchField id="demo-q" label="A field" placeholder="river, mirão…" bind:value={demoQuery} />
		</div>

		<div class="specimen-block">
			<h3 class="sub">Line</h3>
			<p class="big"><Line text="lë Miraluma miru · mi·rão dë Mar." /></p>
		</div>

		<div class="specimen-block">
			<h3 class="sub">Interlinear</h3>
			<Interlinear text="aswen tu velu · solenha." />
		</div>

		<div class="specimen-block">
			<h3 class="sub">EntryRow</h3>
			{#if thalire}<EntryRow entry={thalire} />{/if}
		</div>

		<div class="specimen-block">
			<h3 class="sub">PhraseList</h3>
			<PhraseList phrases={language.phrases.slice(0, 2)} />
		</div>
	</div>
</Section>

<style>
	.intro,
	.lede {
		max-width: 40em;
		display: grid;
		gap: var(--space-xs);
	}
	.sub {
		font-size: var(--step-0);
		color: var(--color-ink-muted);
		font-style: italic;
	}
	.swatches {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-s) var(--space-m);
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 14rem), 1fr));
	}
	.swatches.compact {
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 9rem), 1fr));
	}
	.swatches li {
		display: grid;
		gap: 0.1rem;
		font-size: var(--step--1);
	}
	.swatches code {
		justify-self: start;
	}
	.swatch {
		height: 3.25rem;
		border-radius: var(--radius-m);
		border: var(--rule);
	}
	.compact .swatch {
		height: 2.25rem;
	}
	.value,
	.note {
		color: var(--color-ink-muted);
	}
	.note {
		font-style: italic;
	}
	.stress-demo {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--space-s) var(--space-l);
		line-height: 1.1;
		--stress-offset: 0.12em;
	}
	.scale,
	.space,
	.motion {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-s);
	}
	.scale li {
		display: grid;
		gap: 0.1rem;
		border-bottom: var(--rule);
		padding-bottom: var(--space-xs);
		min-width: 0;
	}
	.meta {
		font-size: var(--step--1);
		display: flex;
		flex-wrap: wrap;
		gap: 0 var(--space-xs);
	}
	.specimen {
		line-height: var(--leading-tight);
		overflow-wrap: anywhere;
	}
	.specimen i {
		color: var(--color-ink-muted);
	}
	.space li {
		display: grid;
		grid-template-columns: minmax(0, 7rem) auto 1fr;
		align-items: center;
		gap: var(--space-s);
		font-size: var(--step--1);
	}
	.bar {
		height: 0.75rem;
		background: var(--color-accent);
		border-radius: 2px;
	}
	.motion li {
		font-size: var(--step--1);
	}
	.breathe-demo {
		display: grid;
		gap: var(--space-s);
		justify-items: start;
	}
	.breathing {
		font-size: var(--step-4);
		line-height: 1.1;
	}
	.specimens {
		display: grid;
		gap: var(--space-l);
	}
	.specimen-block {
		display: grid;
		gap: var(--space-xs);
		padding: var(--space-m);
		border: var(--rule);
		border-radius: var(--radius-m);
	}
	.row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-s);
		align-items: center;
	}
	.big {
		font-size: var(--step-2);
	}
</style>
