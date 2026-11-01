<script lang="ts">
	import { resolve } from '$app/paths';
	import ThemeToggle from '$components/ui/ThemeToggle.svelte';
	import { language } from '$lib/language';
</script>

<footer>
	<div class="wrap row">
		<a href={resolve('/unspoken')}>unspoken words</a>
		<a href={resolve('/principles')}>principles</a>
		<a href={resolve('/design')}>design system</a>
		<a href="https://github.com/oddurs/calenha">source</a>
		<ThemeToggle />
		<span>built {language.meta.built} from the language’s own data</span>
	</div>
</footer>

<style>
	footer {
		border-top: var(--rule);
		color: var(--color-ink-muted);
		font-size: var(--step--1);
		padding-block: var(--space-m) var(--space-xl);
		margin-top: var(--space-2xl);
	}
	.row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-m);
	}
</style>
