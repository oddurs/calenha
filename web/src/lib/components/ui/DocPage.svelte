<!--
  @component
  A page made from one of the language's documents.
-->
<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import type { Doc } from '$lib/language';
	import PageHeader from './PageHeader.svelte';
	import Prose from './Prose.svelte';

	let { doc }: { doc: Doc } = $props();
</script>

<Meta title={doc.title} description={doc.lede} />
<PageHeader title={doc.title} lede={doc.lede} />
<Prose html={doc.html} />
