<!--
  @component
  Every page, by section, each named in Calenha and English; the hour; the source.
-->
<script lang="ts">
	import { language } from '$lib/language';
	import { href, sections } from '$lib/sections';
	import HourControl from './HourControl.svelte';
</script>

<footer>
	<div class="frame margined">
		<div class="margin about">
			<p class="name" lang="x-calenha">calenha</p>
			<p>the calm speech</p>
		</div>
		<div class="main body">
			<nav class="map" aria-label="Every page">
				{#each sections as section (section.english)}
					<div>
						<h2>{section.english}</h2>
						<ul>
							{#each section.pages as p (p.path)}
								<li>
									<a href={href(p.path)}
										><span lang="x-calenha">{p.calenha}</span>
										<span class="en">{p.english}</span></a
									>
								</li>
							{/each}
						</ul>
					</div>
				{/each}
			</nav>
			<HourControl />
			<p class="small">
				{language.meta.counts.words} words, built {language.meta.built} from the language’s own data.
				<a href="https://github.com/oddurs/calenha">Source on GitHub</a>.
			</p>
		</div>
	</div>
</footer>

<style>
	footer {
		margin-top: var(--space-2xl);
		padding-block: var(--space-l) var(--space-xl);
		background: var(--color-surface);
		color: var(--color-ink);
	}
	.about {
		display: grid;
		gap: 0.1rem;
		align-content: start;
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.name {
		font-size: var(--step-2);
		line-height: 1;
		color: var(--color-ink);
	}
	.body {
		display: grid;
		gap: var(--space-l);
	}
	.map {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: var(--space-m);
	}
	h2 {
		font-size: var(--step--1);
		font-weight: 500;
		color: var(--color-ink-muted);
		padding-bottom: var(--space-2xs);
	}
	ul {
		list-style: none;
		padding: 0;
		display: grid;
		gap: var(--space-3xs);
	}
	ul a {
		text-decoration: none;
		display: inline-flex;
		align-items: baseline;
		gap: 0.45em;
		flex-wrap: wrap;
	}
	ul a:hover [lang] {
		text-decoration: underline;
		text-decoration-color: var(--color-accent);
		text-underline-offset: 0.2em;
	}
	[lang='x-calenha'] {
		font-size: 1.08em;
	}
	.en {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	.small {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	@media (max-width: 760px) {
		.about {
			padding-bottom: var(--space-m);
		}
		.map {
			grid-template-columns: repeat(2, minmax(0, 1fr));
			row-gap: var(--space-l);
		}
	}
</style>
