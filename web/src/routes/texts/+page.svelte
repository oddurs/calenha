<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import LinkList from '$components/ui/LinkList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import { language } from '$lib/language';
	import { textHref } from '$lib/links';

	const items = language.texts.map((t) => ({
		label: t.title,
		href: textHref(t.slug),
		note: `${t.english}, a ${t.kind}`,
		lang: 'x-calenha'
	}));
</script>

<Meta title="texts" description="Poems, stories and blessings in Calenha." />
<PageHeader title="texts" lede="Longer pieces of Calenha, to be read slowly and aloud." />
<LinkList {items} />
