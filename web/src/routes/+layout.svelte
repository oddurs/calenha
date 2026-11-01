<script lang="ts">
	import '@fontsource/gentium-book-plus/400.css';
	import '@fontsource/gentium-book-plus/400-italic.css';
	import '@fontsource/gentium-book-plus/700.css';
	import '$design/tokens.css';
	import '$design/base.css';

	import SiteFooter from '$components/layout/SiteFooter.svelte';
	import SiteHeader from '$components/layout/SiteHeader.svelte';
	import SkipLink from '$components/layout/SkipLink.svelte';

	let { children } = $props();
</script>

<SkipLink />
<SiteHeader />
<main id="main" class="wrap">
	{@render children()}
</main>
<SiteFooter />
