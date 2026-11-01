<!--
  @component
  The name of the language and the ways into it.
-->
<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';

	const nav = [
		{ label: 'words', href: resolve('/words') },
		{ label: 'roots', href: resolve('/roots') },
		{ label: 'grammar', href: resolve('/grammar') },
		{ label: 'sounds', href: resolve('/sounds') },
		{ label: 'phrases', href: resolve('/phrases') },
		{ label: 'texts', href: resolve('/texts') },
		{ label: 'reader', href: resolve('/reader') },
		{ label: 'history', href: resolve('/history') },
		{ label: 'world', href: resolve('/world') }
	];

	const here = (href: string) =>
		page.url.pathname === href || page.url.pathname.startsWith(`${href}/`);
</script>

<header class="top">
	<div class="wrap row">
		<a class="home" href={resolve('/')}>calenha</a>
		<nav aria-label="Sections">
			{#each nav as item (item.href)}
				<a href={item.href} aria-current={here(item.href) ? 'page' : undefined}>{item.label}</a>
			{/each}
		</nav>
	</div>
</header>

<style>
	.top {
		padding-block: var(--space-m);
	}
	.row {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: space-between;
		gap: var(--space-2xs) var(--space-m);
	}
	.home {
		font-weight: 700;
		color: var(--color-accent);
		text-decoration: none;
		font-size: 1.2rem;
	}
	nav {
		display: flex;
		flex-wrap: wrap;
		gap: 0.15rem 1.1rem;
		font-size: 1rem;
	}
	nav a {
		color: var(--color-ink-muted);
		text-decoration: none;
	}
	nav a:hover,
	nav a[aria-current='page'] {
		color: var(--color-ink);
	}
	nav a[aria-current='page'] {
		text-decoration: underline;
		text-decoration-color: var(--color-accent);
	}
</style>
