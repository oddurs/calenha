<!--
  @component
  Follow the sun, or choose an hour. Remembered in this browser only.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import Tabs from '$components/ui/Tabs.svelte';
	import { HOURS, hourInfo, pickHour, STORAGE_KEY, type HourChoice } from '$design/hours';

	let choice = $state<HourChoice>('sun');

	onMount(() => {
		const saved = document.documentElement.dataset.hourChoice;
		if (saved && (HOURS as readonly string[]).includes(saved)) choice = saved as HourChoice;
	});

	const options: { value: HourChoice; label: string; title?: string; lang?: string }[] = [
		{ value: 'sun', label: 'follow the sun' },
		...HOURS.map((h) => ({
			value: h as HourChoice,
			label: hourInfo[h].word,
			title: hourInfo[h].english,
			lang: 'x-calenha'
		}))
	];

	function choose(next: HourChoice) {
		const root = document.documentElement;
		const dark = matchMedia('(prefers-color-scheme: dark)').matches;
		root.dataset.hour = pickHour(next === 'sun' ? null : next, new Date().getHours(), dark);
		root.dataset.hourChoice = next;
		try {
			if (next === 'sun') localStorage.removeItem(STORAGE_KEY);
			else localStorage.setItem(STORAGE_KEY, next);
		} catch {
			// not remembered, but shown
		}
	}
</script>

<div class="hour">
	<p>the hour</p>
	<Tabs label="The hour" {options} bind:value={choice} size="small" onchange={choose} />
</div>

<style>
	.hour {
		display: grid;
		gap: var(--space-3xs);
	}
	p {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
</style>
