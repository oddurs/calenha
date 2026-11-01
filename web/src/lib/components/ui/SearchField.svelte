<!--
  @component
  A quiet, underlined text field with its label above.
-->
<script lang="ts">
	interface Props {
		id: string;
		label: string;
		placeholder?: string;
		value: string;
		multiline?: boolean;
	}

	let { id, label, placeholder = '', value = $bindable(), multiline = false }: Props = $props();
</script>

<div class="field">
	<label for={id}>{label}</label>
	{#if multiline}
		<textarea {id} rows="3" spellcheck="false" autocomplete="off" {placeholder} bind:value
		></textarea>
	{:else}
		<input {id} type="search" spellcheck="false" autocomplete="off" {placeholder} bind:value />
	{/if}
</div>

<style>
	.field {
		display: grid;
		gap: var(--space-2xs);
	}
	label {
		color: var(--color-ink-muted);
		font-size: var(--step--1);
	}
	input,
	textarea {
		font: inherit;
		font-size: var(--step-1);
		color: var(--color-ink);
		width: 100%;
	}
	input {
		background: transparent;
		border: 0;
		border-bottom: 1px solid var(--color-ink-muted);
		border-radius: 0;
		padding: 0.3rem 0;
	}
	input:focus {
		outline: none;
		border-bottom-color: var(--color-accent);
		box-shadow: 0 1px 0 var(--color-accent);
	}
	textarea {
		background: var(--color-surface);
		border: var(--rule);
		border-radius: var(--radius-m);
		padding: 0.6rem 0.75rem;
		line-height: var(--leading-snug);
		resize: vertical;
	}
	textarea:focus {
		outline: none;
		border-color: var(--color-accent);
	}
	::placeholder {
		color: var(--color-ink-muted);
		opacity: 0.75;
	}
</style>
