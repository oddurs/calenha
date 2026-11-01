<script lang="ts">
	import '@fontsource-variable/alegreya/wght.css';
	import '@fontsource-variable/alegreya/wght-italic.css';
	import '@fontsource/alegreya-sans/400.css';
	import '@fontsource/alegreya-sans/400-italic.css';
	import '@fontsource/alegreya-sans/500.css';
	import '@fontsource/alegreya-sans/700.css';
	import '@fontsource/noto-serif/400.css';
	import '$design/tokens.css';
	import '$design/base.css';

	import { base } from '$app/paths';
	import { page } from '$app/state';
	import SectionNav from '$components/layout/SectionNav.svelte';
	import SiteFooter from '$components/layout/SiteFooter.svelte';
	import SiteHeader from '$components/layout/SiteHeader.svelte';
	import SkipLink from '$components/layout/SkipLink.svelte';

	let { children } = $props();

	const home = $derived(
		page.url.pathname === `${base}/` || page.url.pathname === base || page.url.pathname === '/'
	);
</script>

<SkipLink />
<SiteHeader tone={home ? 'sky' : 'page'} />
{#if !home}<SectionNav />{/if}
<main id="main" class:frame={!home}>
	{@render children()}
</main>
<SiteFooter />
