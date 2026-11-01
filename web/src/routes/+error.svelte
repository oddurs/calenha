<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import Meta from '$components/layout/Meta.svelte';
	import Line from '$components/language/Line.svelte';
</script>

<Meta title="nothing here" description="There is no page at this address." />

<div class="lost margined">
	<p class="margin code">{page.status}</p>
	<div class="main">
		<p class="cal"><Line text="nã · nada acá." /></p>
		<p class="tr">Nothing here.</p>
		<p>
			{page.status === 404 ? 'There is no page at this address.' : page.error?.message}
			Try the <a href={resolve('/words')}>dictionary</a>, or go back to the
			<a href={resolve('/')}>beginning</a>.
		</p>
	</div>
</div>

<style>
	.lost {
		padding-block: var(--space-2xl);
		align-items: baseline;
	}
	.code {
		color: var(--color-ink-muted);
	}
	.main {
		display: grid;
		gap: var(--space-xs);
	}
	.cal {
		font-size: var(--step-5);
		line-height: 1.1;
	}
	.tr {
		font-size: var(--step-2);
		font-style: italic;
	}
</style>
