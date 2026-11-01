<script lang="ts">
	import Meta from '$components/layout/Meta.svelte';
	import PhraseList from '$components/language/PhraseList.svelte';
	import PageHeader from '$components/ui/PageHeader.svelte';
	import Section from '$components/ui/Section.svelte';
	import { language, plain } from '$lib/language';

	const groups = language.topics
		.map((topic) => ({ topic, phrases: language.phrases.filter((p) => p.topic === topic) }))
		.filter((g) => g.phrases.length);
</script>

<Meta
	title="phrases"
	description="A phrasebook of Calenha: greetings, the hours, the heart, land and sea, sayings."
/>

<PageHeader
	english="phrases"
	calenha="fala"
	lede="Things to say. Each line in Calenha, then what it means, then the words one by one."
/>

{#each groups as g (g.topic)}
	<Section id="t-{plain(g.topic).replaceAll(' ', '-')}" title={g.topic}>
		<PhraseList phrases={g.phrases} />
	</Section>
{/each}
