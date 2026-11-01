<!--
  @component
  The page's name in the tab, and its one-line description.
-->
<script lang="ts">
	interface Props {
		title?: string;
		description: string;
	}

	let { title, description }: Props = $props();
</script>

<svelte:head>
	<title>{title ? `${title} – Calenha` : 'Calenha'}</title>
	<meta name="description" content={description} />
</svelte:head>
