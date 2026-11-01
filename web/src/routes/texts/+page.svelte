<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import LinkList from '$components/ui/LinkList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import { language } from '$lib/language';
	import { textHref } from '$lib/links';

	const items = language.texts.map((t) => ({
		href: textHref(t.slug),
		calenha: t.title,
		english: t.english,
		note: `a ${t.kind}, ${t.lines.filter((l) => l.text.trim()).length} lines`
	}));
</script>

<Meta title="texts" description="Poems, stories and blessings in Calenha." />

<PageHeader english="texts" calenha="lenda" lede="Longer pieces, to be read slowly and aloud." />

<div class="margined"><div class="main"><LinkList {items} /></div></div>
