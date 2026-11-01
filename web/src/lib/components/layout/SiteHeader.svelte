<!--
  @component
  The name of the language and its four sections. The wordmark is the word itself,
  with its beat — the identity is the language's own stress.
-->
<script lang="ts">
	import { base, resolve } from '$app/paths';
	import { page } from '$app/state';
	import Word from '$components/language/Word.svelte';
	import { lookup } from '$lib/language';
	import { href, sectionOf, sections } from '$lib/sections';

	let { tone = 'page' }: { tone?: 'page' | 'sky' } = $props();

	const name = lookup('calenha');
	const current = $derived(sectionOf(page.url.pathname, base));
</script>

<header class="top {tone}">
	<div class="frame margined row">
		<a class="margin wordmark" href={resolve('/')} aria-label="Calenha, home">
			{#if name}<Word shape={name} />{/if}
		</a>
		<nav class="main" aria-label="Sections">
			{#each sections as section (section.english)}
				<a
					href={href(section.pages[0]?.path ?? '/')}
					aria-current={current === section ? 'true' : undefined}>{section.english}</a
				>
			{/each}
		</nav>
	</div>
</header>

<style>
	.top {
		padding-block: var(--space-m) var(--space-s);
	}
	.sky {
		background: var(--horizon-sky);
		color: var(--color-on-sky);
	}
	.row {
		align-items: baseline;
		row-gap: var(--space-2xs);
	}
	.wordmark {
		font-size: 1.65rem;
		line-height: 1;
		text-decoration: none;
		justify-self: start;
	}
	nav {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3xs) var(--space-l);
	}
	nav a {
		font-size: var(--step-0);
		font-weight: 500;
		text-decoration: underline;
		text-decoration-color: transparent;
		text-decoration-thickness: 2px;
		text-underline-offset: 0.4em;
		opacity: 0.78;
		transition:
			opacity var(--duration-quick) var(--ease-tide),
			text-decoration-color var(--duration-quick) var(--ease-tide);
	}
	nav a:hover {
		opacity: 1;
	}
	nav a[aria-current] {
		opacity: 1;
		text-decoration-color: var(--color-accent);
	}
	.sky nav a[aria-current] {
		text-decoration-color: currentColor;
	}
	@media (max-width: 760px) {
		nav {
			gap: var(--space-3xs) var(--space-m);
		}
	}
</style>
