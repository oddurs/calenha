<!--
  @component
  A long document rendered from the language's own Markdown. The HTML is produced
  by `calenha export` from files in this repository, so it is trusted.
-->
<script lang="ts">
	let { html }: { html: string } = $props();
</script>

<div class="prose">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted: rendered from the repo's own docs -->
	{@html html}
</div>

<style>
	.prose {
		max-width: 40em;
		display: grid;
		gap: var(--space-s);
	}
	.prose :global(h2) {
		font-size: var(--step-2);
		color: var(--color-accent);
		padding-top: var(--space-l);
		scroll-margin-top: var(--space-m);
	}
	.prose :global(h3) {
		font-size: var(--step-1);
		padding-top: var(--space-s);
	}
	.prose :global(ul),
	.prose :global(ol) {
		padding-left: 1.25rem;
		display: grid;
		gap: var(--space-2xs);
	}
	.prose :global(blockquote) {
		padding: var(--space-3xs) 0 var(--space-3xs) var(--space-m);
		border-left: 2px solid var(--color-rule);
		display: grid;
		gap: var(--space-2xs);
	}
	.prose :global(blockquote strong) {
		font-weight: 400;
		font-size: 1.15em;
	}
	.prose :global(strong) {
		font-weight: 700;
	}
	.prose :global(.table) {
		overflow-x: auto;
	}
	.prose :global(table) {
		border-collapse: collapse;
		width: 100%;
		font-size: var(--step--1);
	}
	.prose :global(th) {
		text-align: left;
		font-weight: 400;
		font-style: italic;
		color: var(--color-ink-muted);
	}
	.prose :global(th),
	.prose :global(td) {
		padding: 0.45rem 0.9rem 0.45rem 0;
		border-bottom: var(--rule);
		vertical-align: top;
	}
</style>
