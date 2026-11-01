<!--
  @component
  The pages of the current section, beneath the header.
-->
<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import { href, sectionOf } from '$lib/sections';

	const section = $derived(sectionOf(page.url.pathname, base));
	const here = (path: string) => {
		const p = page.url.pathname.slice(base.length);
		return p === path || p.startsWith(`${path}/`);
	};
</script>

{#if section}
	<nav class="frame margined sub" aria-label="{section.english} pages">
		<p class="margin" lang="x-calenha">{section.calenha}</p>
		<ul class="main">
			{#each section.pages as p (p.path)}
				<li>
					<a href={href(p.path)} aria-current={here(p.path) ? 'page' : undefined}>{p.english}</a>
				</li>
			{/each}
		</ul>
	</nav>
{/if}

<style>
	.sub {
		padding-block: var(--space-2xs) 0;
		align-items: baseline;
	}
	p {
		color: var(--color-ink-muted);
		font-size: var(--step-1);
		line-height: 1;
	}
	ul {
		list-style: none;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3xs) var(--space-m);
		border-bottom: var(--rule);
	}
	a {
		display: inline-block;
		padding-block: var(--space-xs);
		color: var(--color-ink-muted);
		text-decoration: none;
		border-bottom: 2px solid transparent;
		margin-bottom: -1px;
	}
	a:hover {
		color: var(--color-ink);
	}
	a[aria-current='page'] {
		color: var(--color-ink);
		border-bottom-color: var(--color-accent);
	}
	@media (max-width: 760px) {
		p {
			display: none;
		}
	}
</style>
