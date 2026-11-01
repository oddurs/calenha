<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import Meta from '$components/layout/Meta.svelte';
	import Line from '$components/language/Line.svelte';
</script>

<Meta title="nã" description="There is no page here." />

<div class="lost">
	<p class="cal"><Line text="nã · nada acá." /></p>
	<p class="translation">Nothing here.</p>
	<p>
		{page.status === 404 ? 'There is no page at this address.' : page.error?.message}
		Try the <a href={resolve('/words')}>words</a> or go <a href={resolve('/')}>home</a>.
	</p>
</div>

<style>
	.lost {
		padding-block: var(--space-2xl);
		display: grid;
		gap: var(--space-xs);
	}
	.cal {
		font-size: var(--step-5);
		line-height: 1.1;
	}
	.translation {
		font-style: italic;
		color: var(--color-ink-muted);
		font-size: var(--step-1);
	}
</style>
