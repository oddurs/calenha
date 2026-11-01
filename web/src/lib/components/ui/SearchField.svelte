<!--
  @component
  A text field with its label. `lang="x-calenha"` sets what is typed in Calenha's voice.
-->
<script lang="ts">
	interface Props {
		id: string;
		label: string;
		placeholder?: string;
		value: string;
		multiline?: boolean;
		lang?: string;
		hideLabel?: boolean;
	}

	let {
		id,
		label,
		placeholder = '',
		value = $bindable(),
		multiline = false,
		lang,
		hideLabel = false
	}: Props = $props();
</script>

<div class="field">
	<label for={id} class:visually-hidden={hideLabel}>{label}</label>
	{#if multiline}
		<textarea {id} {lang} rows="2" spellcheck="false" autocomplete="off" {placeholder} bind:value
		></textarea>
	{:else}
		<input
			{id}
			{lang}
			type="search"
			spellcheck="false"
			autocomplete="off"
			{placeholder}
			bind:value
		/>
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
		font-size: var(--step-2);
		line-height: var(--leading-snug);
		color: var(--color-ink);
		width: 100%;
		background: transparent;
		border: 0;
		border-bottom: 1px solid var(--field-line);
		border-radius: 0;
		padding: 0.25rem 0 0.45rem;
		resize: vertical;
	}
	input:lang(x-calenha),
	textarea:lang(x-calenha) {
		font-family: var(--font-calenha);
	}
	input:focus,
	textarea:focus {
		outline: none;
		border-bottom-color: var(--field-line-focus);
		box-shadow: 0 1px 0 var(--field-line-focus);
	}
	::placeholder {
		color: var(--color-ink-muted);
		opacity: 0.7;
	}
	input::-webkit-search-cancel-button {
		filter: grayscale(1);
	}
</style>
