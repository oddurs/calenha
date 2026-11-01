<!--
  @component
  Choose one of a few: filters, reading modes, the hour. The chosen one is in ink
  with a mark beneath; the rest are quiet. One selection pattern for the whole site.
-->
<script lang="ts" generics="T extends string">
	interface Option {
		value: T;
		label: string;
		title?: string;
		/** 'x-calenha' when the label is a Calenha word */
		lang?: string;
	}

	interface Props {
		label: string;
		options: Option[];
		value: T;
		size?: 'normal' | 'small';
		onchange?: (value: T) => void;
	}

	let { label, options, value = $bindable(), size = 'normal', onchange }: Props = $props();
</script>

<div class="tabs {size}" role="group" aria-label={label}>
	{#each options as option (option.value)}
		<button
			type="button"
			lang={option.lang}
			title={option.title}
			aria-pressed={option.value === value}
			onclick={() => {
				value = option.value;
				onchange?.(option.value);
			}}>{option.label}</button
		>
	{/each}
</div>

<style>
	.tabs {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2xs) var(--space-m);
	}
	button {
		font: inherit;
		font-size: var(--step-0);
		line-height: 1.4;
		color: var(--tab-ink);
		background: none;
		border: 0;
		padding: 0.15rem 0;
		cursor: pointer;
		text-decoration: underline;
		text-decoration-color: transparent;
		text-decoration-thickness: 2px;
		text-underline-offset: 0.35em;
		transition:
			color var(--duration-quick) var(--ease-tide),
			text-decoration-color var(--duration-quick) var(--ease-tide);
	}
	button:lang(x-calenha) {
		font-family: var(--font-calenha);
		font-size: 1.08em;
	}
	.small button {
		font-size: var(--step--1);
	}
	button:hover {
		color: var(--tab-ink-current);
		text-decoration-color: var(--color-rule);
	}
	button[aria-pressed='true'] {
		color: var(--tab-ink-current);
		text-decoration-color: var(--tab-mark);
	}
</style>
