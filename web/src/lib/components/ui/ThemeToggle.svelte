<!--
  @component
  Follow the system, or choose light or dark. The choice is remembered in this
  browser only, and applied before first paint by a script in app.html.
-->
<script lang="ts">
	import { onMount } from 'svelte';

	type Theme = 'system' | 'light' | 'dark';
	const KEY = 'calenha:theme';
	const order: Theme[] = ['system', 'light', 'dark'];

	let theme = $state<Theme>('system');

	onMount(() => {
		try {
			const saved = localStorage.getItem(KEY);
			if (saved === 'light' || saved === 'dark') theme = saved;
		} catch {
			// storage may be unavailable; the system theme still applies
		}
	});

	function next() {
		theme = order[(order.indexOf(theme) + 1) % order.length] ?? 'system';
		const root = document.documentElement;
		if (theme === 'system') delete root.dataset.theme;
		else root.dataset.theme = theme;
		try {
			if (theme === 'system') localStorage.removeItem(KEY);
			else localStorage.setItem(KEY, theme);
		} catch {
			// not remembered, but applied
		}
	}
</script>

<button type="button" class="theme" onclick={next} aria-label="Theme: {theme}. Change theme">
	{theme === 'system' ? 'theme follows the system' : `${theme} theme`}
</button>

<style>
	.theme {
		font: inherit;
		color: inherit;
		background: none;
		border: 0;
		padding: 0;
		cursor: pointer;
		text-decoration: underline;
		text-decoration-color: var(--color-rule);
		text-underline-offset: 0.2em;
	}
	.theme:hover {
		text-decoration-color: var(--color-accent);
	}
</style>
