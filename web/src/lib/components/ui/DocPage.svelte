<!--
  @component
  A page made from one of the language's documents.
-->
<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import type { Doc } from '$lib/language';
	import PageHeader from './PageHeader.svelte';
	import Prose from './Prose.svelte';

	interface Props {
		doc: Doc;
		english: string;
		calenha: string;
	}

	let { doc, english, calenha }: Props = $props();
</script>

<Meta title={english} description={doc.lede} />
<PageHeader {english} {calenha} lede={doc.lede} />
<Prose html={doc.html} />
