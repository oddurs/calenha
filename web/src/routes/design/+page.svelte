<script lang="ts">
	import { onMount } from 'svelte';
	import Horizon from '$components/layout/Horizon.svelte';
	import Meta from '$components/layout/Meta.svelte';
	import EntryRow from '$components/language/EntryRow.svelte';
	import Interlinear from '$components/language/Interlinear.svelte';
	import Line from '$components/language/Line.svelte';
	import PhraseList from '$components/language/PhraseList.svelte';
	import Word from '$components/language/Word.svelte';
	import Button from '$components/ui/Button.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import SearchField from '$components/ui/SearchField.svelte';
	import Section from '$components/ui/Section.svelte';
	import Tabs from '$components/ui/Tabs.svelte';
	import { HOURS, hourInfo } from '$design/hours';
	import { motion, primitives, roles, space, typeScale } from '$design/tokens';
	import { language, lookup } from '$lib/language';

	// values live only in tokens.css; read them from the page once it is drawn
	let values = $state<Record<string, string>>({});
	onMount(() => {
		const style = getComputedStyle(document.documentElement);
		const names = [
			...primitives.flatMap((p) => p.tokens),
			...typeScale.map((t) => t.name),
			...space.map((t) => t.name),
			...motion.map((t) => t.name)
		];
		values = Object.fromEntries(names.map((n) => [n, style.getPropertyValue(n).trim()]));
	});

	const thalire = lookup('thalírë');
	const miraluma = lookup('miraluma');
	let demoQuery = $state('');
	let demoTab = $state('una');
	let replay = $state(0);
</script>

<Meta
	title="design"
	description="The Calenha design system: hours, two voices, the beat, type, space, motion and components."
/>

<PageHeader
	english="design"
	calenha="fazu"
	lede="How this site is made. Fog, sea and one poppy; two voices; and a page that keeps Calenha time."
/>

<Section id="layers" title="three layers">
	<div class="cols">
		<div>
			<h3>primitives</h3>
			<p>
				The raw palette and scales, named for things in Solmara: fog, pacific, sage, rose, amber,
				poppy. Never used by a component directly.
			</p>
		</div>
		<div>
			<h3>semantic</h3>
			<p>
				Roles: page, ink, accent, rule, beat, sky, haze, sea. The only layer that changes, and it
				changes with the hour.
			</p>
		</div>
		<div>
			<h3>component</h3>
			<p>
				Decisions particular to one component, built from roles, and recomputed wherever an hour is
				set, so they follow it.
			</p>
		</div>
	</div>
	<p class="muted">
		All values live in <code>src/lib/design/tokens.css</code>. This page shows them live; each hour
		below is the real token set, applied to a part of the page.
	</p>
</Section>

<Section id="hours" title="the hours">
	<p class="lead">
		In place of light and dark, the site has five hours. Following the sun, it picks one from your
		clock; a dark system means night. Choose one at the foot of any page.
	</p>
	<div class="hours">
		{#each HOURS as h (h)}
			<figure data-hour={h} class="hour">
				<Horizon compact label="{hourInfo[h].english}: sky and sea">
					{#snippet sky()}<p class="mini" lang="x-calenha">{hourInfo[h].word}</p>{/snippet}
					{#snippet sea()}<p class="mini-en">{hourInfo[h].english}</p>{/snippet}
				</Horizon>
				<figcaption>
					<p class="sample">
						<span lang="x-calenha"
							>{#if thalire}<Word shape={thalire} />{/if}</span
						> river
					</p>
					<p class="note">{hourInfo[h].note}</p>
				</figcaption>
			</figure>
		{/each}
	</div>

	<div class="table">
		<table class="matrix">
			<thead>
				<tr>
					<th scope="col">role</th>
					{#each HOURS as h (h)}<th scope="col" lang="x-calenha">{hourInfo[h].word}</th>{/each}
				</tr>
			</thead>
			<tbody>
				{#each roles as role (role.name)}
					<tr>
						<th scope="row"><code>{role.name}</code><span>{role.note}</span></th>
						{#each HOURS as h (h)}
							<td data-hour={h}><span class="chip" style:background="var({role.name})"></span></td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
	<p class="muted">
		Every pair of text and ground meets WCAG AA in every hour; ink on page is above 13:1.
	</p>
</Section>

<Section id="primitives" title="primitives">
	<div class="families">
		{#each primitives as fam (fam.family)}
			<div class="family">
				<p><b>{fam.family}</b> <span class="muted">{fam.note}</span></p>
				<ul class="ramp">
					{#each fam.tokens as t (t)}
						<li style:background="var({t})" title="{t} {values[t] ?? ''}">
							<span>{t.split('-').at(-1)}</span>
						</li>
					{/each}
				</ul>
			</div>
		{/each}
	</div>
</Section>

<Section id="voices" title="two voices">
	<p class="lead">
		Calenha always speaks in Alegreya, a calligraphic serif. English speaks in Alegreya Sans, its
		humanist sibling. The rule is keyed to the <code>lang</code> attribute, so anything tagged
		<code>x-calenha</code> takes the serif on its own, and the type tells you which language you are reading.
		IPA is set in Noto Serif, which carries every symbol.
	</p>
	<div class="voices">
		<div>
			<p class="specimen-cal" lang="x-calenha">tardë morna · brisa fria · Mar lenta.</p>
			<p class="specimen-label">Calenha, in Alegreya</p>
		</div>
		<div>
			<p class="specimen-en">A warm afternoon, a cool breeze, the slow sea.</p>
			<p class="specimen-label">English, in Alegreya Sans</p>
		</div>
		<div>
			<p class="specimen-ipa ipa">/ˈtaɾ.de ˈmɔɾ.na ˈbɾi.za ˈfɾi.a maɾ ˈlɛn.ta/</p>
			<p class="specimen-label">IPA, in Noto Serif</p>
		</div>
	</div>
</Section>

<Section id="beat" title="the beat">
	<p class="lead">
		A short poppy bar over the stressed syllable: the system's one bright mark, and it only ever
		means stress. It shows where a word stands alone, as on a word's page, in the dictionary and in
		word-by-word reading. In running lines it waits for you to point at a word, so the writing stays
		clean.
	</p>
	{#if thalire && miraluma}
		<div class="beats">
			<span style:font-size="var(--step-6)"><Word shape={thalire} /></span>
			<span style:font-size="var(--step-4)"><Word shape={miraluma} shown="Miraluma" /></span>
			<span style:font-size="var(--step-2)"><Word shape={thalire} /></span>
		</div>
	{/if}
	<p class="line-demo"><Line text="lë Miraluma miru · mi·rão dë Mar." /></p>
	<p class="muted">Point at a word in the line above to see its beat and meaning.</p>
</Section>

<Section id="type" title="type scale">
	<ul class="scale">
		{#each typeScale as step (step.name)}
			<li>
				<p class="meta">
					<code>{step.name}</code> <span class="muted">{values[step.name] ?? ''}</span>
					<i class="muted">{step.note}</i>
				</p>
				<p class="specimen" style:font-size="var({step.name})">
					<span lang="x-calenha">solenha</span> dappled light
				</p>
			</li>
		{/each}
	</ul>
</Section>

<Section id="space" title="space">
	<p class="muted">
		Siblings are spaced with gap, never margins, and every page sits on the margin grid: a narrow
		column for labels beside a main column for reading.
	</p>
	<ul class="space">
		{#each space as step (step.name)}
			<li>
				<code>{step.name}</code>
				<span class="bar" style:width="var({step.name})"></span>
				<span class="muted">{values[step.name] ?? ''} {step.note}</span>
			</li>
		{/each}
	</ul>
</Section>

<Section id="motion" title="motion">
	<p class="lead">
		One orchestrated moment: the opening line arrives word by word, once. The hour changes slowly.
		Everything else moves only when you do.
	</p>
	<div class="breathe">
		{#key replay}<p class="breathing"><Line text="onda onda onda" links={false} breathe /></p>{/key}
		<Button onclick={() => replay++}>Breathe again</Button>
	</div>
	<ul class="motion">
		{#each motion as m (m.name)}
			<li>
				<code>{m.name}</code> <span class="muted">{values[m.name] ?? ''}</span>
				<i class="muted">{m.note}</i>
			</li>
		{/each}
	</ul>
</Section>

<Section id="components" title="components">
	<div class="specimens">
		<div class="specimen-row">
			<p class="name">Tabs</p>
			<Tabs
				label="Demo"
				options={[
					{ value: 'una', label: 'una', lang: 'x-calenha' },
					{ value: 'dua', label: 'dua', lang: 'x-calenha' },
					{ value: 'trë', label: 'trë', lang: 'x-calenha' }
				]}
				bind:value={demoTab}
			/>
		</div>
		<div class="specimen-row">
			<p class="name">SearchField</p>
			<SearchField id="demo-q" label="A field" placeholder="river, mirão" bind:value={demoQuery} />
		</div>
		<div class="specimen-row">
			<p class="name">Interlinear</p>
			<Interlinear text="aswen tu velu · solenha." />
		</div>
		<div class="specimen-row">
			<p class="name">EntryRow</p>
			{#if thalire}<EntryRow entry={thalire} />{/if}
		</div>
		<div class="specimen-row">
			<p class="name">PhraseList</p>
			<PhraseList phrases={language.phrases.slice(0, 2)} />
		</div>
	</div>
</Section>

<style>
	.lead {
		font-size: var(--step-1);
		line-height: 1.45;
		max-width: 34em;
	}
	.muted {
		color: var(--color-ink-muted);
	}
	h3 {
		font-size: var(--step-0);
		font-weight: 700;
	}
	.cols {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: var(--space-l);
	}
	.cols > div {
		display: grid;
		gap: var(--space-3xs);
		align-content: start;
		border-top: 2px solid var(--color-ink);
		padding-top: var(--space-xs);
	}

	.hours {
		display: grid;
		grid-template-columns: repeat(5, minmax(0, 1fr));
		gap: var(--space-s);
	}
	.hour {
		margin: 0;
		background: var(--color-page);
		color: var(--color-ink);
		border-radius: var(--radius-m);
		overflow: hidden;
		display: grid;
		align-content: start;
		box-shadow: 0 0 0 1px var(--color-rule);
	}
	.mini {
		font-size: var(--step-2);
		line-height: 1;
	}
	.mini-en {
		font-size: var(--step--1);
	}
	figcaption {
		padding: var(--space-s) var(--space-s) var(--space-m);
		display: grid;
		gap: var(--space-3xs);
	}
	.sample {
		font-size: var(--step-1);
	}
	.note {
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}

	.table {
		overflow-x: auto;
	}
	.matrix {
		border-collapse: collapse;
		width: 100%;
		font-size: var(--step--1);
	}
	/* rules on rows, so each hour's cell keeps the page's hairline */
	.matrix tr {
		border-bottom: var(--rule);
	}
	.matrix th,
	.matrix td {
		padding: 0.4rem 0.6rem 0.4rem 0;
		text-align: left;
		font-weight: 400;
		vertical-align: middle;
	}
	.matrix thead th {
		color: var(--color-ink-muted);
		font-size: var(--step-0);
	}
	.matrix tbody th {
		display: grid;
		gap: 0.1rem;
		min-width: 12rem;
	}
	.matrix tbody th code {
		justify-self: start;
	}
	.matrix tbody th span {
		color: var(--color-ink-muted);
	}
	.matrix td {
		background: none;
	}
	.chip {
		display: block;
		height: 2rem;
		min-width: 3rem;
		border-radius: var(--radius-s);
		box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--color-ink) 12%, transparent);
	}

	.families {
		display: grid;
		gap: var(--space-m);
	}
	.family {
		display: grid;
		gap: var(--space-2xs);
	}
	.ramp {
		list-style: none;
		padding: 0;
		display: flex;
		border-radius: var(--radius-m);
		overflow: hidden;
		box-shadow: 0 0 0 1px var(--color-rule);
	}
	.ramp li {
		flex: 1;
		height: 3rem;
		display: flex;
		align-items: end;
		padding: 0.3rem;
	}
	.ramp span {
		font-size: 0.7rem;
		font-family: var(--font-code);
		background: color-mix(in srgb, var(--color-page) 80%, transparent);
		color: var(--color-ink);
		padding: 0 0.2rem;
		border-radius: 2px;
	}

	.voices {
		display: grid;
		gap: var(--space-m);
	}
	.voices > div {
		display: grid;
		gap: var(--space-3xs);
		padding-top: var(--space-s);
		border-top: var(--rule);
	}
	.specimen-cal {
		font-size: var(--step-4);
		line-height: 1.1;
	}
	.specimen-en {
		font-size: var(--step-2);
		line-height: 1.2;
	}
	.specimen-ipa {
		font-size: var(--step-2);
		color: var(--color-accent);
	}
	.specimen-label {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}

	.beats {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--space-s) var(--space-l);
		line-height: 1.1;
		padding-top: var(--space-s);
	}
	.line-demo {
		font-size: var(--step-3);
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
		padding-bottom: var(--space-xs);
		border-bottom: var(--rule);
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
	.space li {
		display: grid;
		grid-template-columns: minmax(0, 7.5rem) auto minmax(0, 1fr);
		align-items: center;
		gap: var(--space-s);
		font-size: var(--step--1);
	}
	.bar {
		height: 0.7rem;
		background: var(--color-accent);
		border-radius: 2px;
	}
	.motion li {
		font-size: var(--step--1);
	}
	.breathe {
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
	}
	.specimen-row {
		display: grid;
		gap: var(--space-s);
		padding-block: var(--space-m);
		border-top: var(--rule);
	}
	.name {
		font-family: var(--font-code);
		font-size: var(--step--1);
		color: var(--color-ink-muted);
	}

	@media (max-width: 1000px) {
		.hours {
			grid-template-columns: repeat(auto-fill, minmax(min(100%, 11rem), 1fr));
		}
	}
	@media (max-width: 640px) {
		.cols {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
