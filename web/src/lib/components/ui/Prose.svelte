<!--
  @component
  A long document rendered from the language's own Markdown. The export tags Calenha
  in it, so examples speak in Calenha's voice. Section headings sit in the margin.
  The HTML comes from files in this repository and is trusted.
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
		display: grid;
		grid-template-columns: var(--margin-column) minmax(0, var(--text-max));
		column-gap: var(--space-l);
		row-gap: var(--space-s);
		align-items: start;
	}
	.prose > :global(*) {
		grid-column: 2;
	}
	/* a section's heading sits in the margin, beside its first paragraph */
	.prose > :global(h2) {
		grid-column: 1;
		font-size: var(--step-0);
		font-weight: 500;
		line-height: 1.4;
		padding-top: 0.15rem;
		scroll-margin-top: var(--space-m);
	}
	.prose > :global(h2 + *) {
		margin-top: 0;
	}
	.prose > :global(h2:not(:first-child)),
	.prose > :global(h2:not(:first-child) + *) {
		margin-top: var(--space-l);
	}
	.prose :global(h3) {
		font-size: var(--step-1);
		padding-top: var(--space-s);
	}
	.prose :global(ul),
	.prose :global(ol) {
		padding-left: 1.2rem;
		display: grid;
		gap: var(--space-2xs);
	}
	.prose :global(li::marker) {
		color: var(--color-ink-muted);
	}
	.prose :global(:lang(x-calenha)) {
		font-style: normal;
		font-weight: 500;
		font-size: 1.1em;
	}
	.prose :global(blockquote) {
		padding: var(--space-xs) 0 var(--space-xs) var(--space-m);
		border-left: 2px solid var(--color-rule);
		display: grid;
		gap: var(--space-2xs);
	}
	.prose :global(blockquote :lang(x-calenha)) {
		font-size: 1.3em;
		font-weight: 400;
	}
	.prose :global(code) {
		white-space: nowrap;
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
		font-weight: 500;
		color: var(--color-ink-muted);
	}
	.prose :global(th),
	.prose :global(td) {
		padding: 0.5rem 1rem 0.5rem 0;
		border-bottom: var(--rule);
		vertical-align: top;
	}
	.prose :global(td :lang(x-calenha)) {
		font-size: 1.25em;
	}
	@media (max-width: 760px) {
		.prose {
			grid-template-columns: minmax(0, 1fr);
		}
		.prose > :global(*),
		.prose > :global(h2) {
			grid-column: 1;
		}
		.prose > :global(h2:not(:first-child)) {
			margin-top: var(--space-l);
		}
		.prose > :global(h2 + *) {
			margin-top: 0 !important;
		}
	}
</style>
