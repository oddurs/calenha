<!--
  @component
  A row of chips where exactly one is chosen.
-->
<script lang="ts" generics="T extends string">
	import Chip from './Chip.svelte';

	interface Props {
		label: string;
		options: { value: T; label: string; title?: string }[];
		value: T;
	}

	let { label, options, value = $bindable() }: Props = $props();
</script>

<div class="group" role="group" aria-label={label}>
	{#each options as option (option.value)}
		<Chip
			pressed={option.value === value}
			title={option.title}
			onclick={() => (value = option.value)}
		>
			{option.label}
		</Chip>
	{/each}
</div>

<style>
	.group {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs);
	}
</style>
