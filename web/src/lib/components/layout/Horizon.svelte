<!--
  @component
  Sky over sea, in the colours of the hour, with the sun (or the moon) where the
  hour puts it. The opening of the site. `sky` sits above the horizon, `sea` below.
-->
<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		sky: Snippet;
		sea?: Snippet;
		compact?: boolean;
		label?: string;
	}

	let { sky, sea, compact = false, label }: Props = $props();
</script>

<div class="horizon" class:compact role={label ? 'img' : undefined} aria-label={label}>
	<div class="sky">
		<span class="sun" aria-hidden="true"></span>
		<div class="frame margined"><div class="main">{@render sky()}</div></div>
	</div>
	<div class="sea">
		<div class="frame margined"><div class="main">{@render sea?.()}</div></div>
	</div>
</div>

<style>
	.horizon {
		position: relative;
		isolation: isolate;
	}
	.sky {
		position: relative;
		isolation: isolate;
		overflow: hidden;
		color: var(--color-on-sky);
		/* light gathers at the horizon: the one gradient on the site, and it is weather */
		background: linear-gradient(
			to bottom,
			var(--horizon-sky) 0%,
			var(--horizon-sky) 55%,
			var(--horizon-haze) 100%
		);
		padding-block: clamp(3rem, 9vw, 7rem) clamp(1.75rem, 4vw, 3rem);
	}
	.sun {
		position: absolute;
		left: var(--sun-x);
		/* never cut off at the top of the sky */
		top: max(var(--sun-y), calc(min(var(--sun-size), 26vw) / 2 + 0.75rem));
		width: min(var(--sun-size), 26vw);
		aspect-ratio: 1;
		max-width: 100%;
		translate: -50% -50%;
		border-radius: 50%;
		background: var(--sun-color);
		opacity: var(--sun-opacity);
		filter: blur(var(--sun-blur));
		z-index: -1;
		transition:
			top 1200ms var(--ease-tide),
			left 1200ms var(--ease-tide),
			width 1200ms var(--ease-tide),
			background-color 1200ms var(--ease-tide);
	}
	.sky .frame {
		position: relative;
	}
	.sea {
		background: var(--horizon-sea);
		color: var(--color-on-sea);
		padding-block: clamp(1.5rem, 3.5vw, 2.5rem) clamp(2rem, 5vw, 3.5rem);
		/* a glint along the horizon */
		box-shadow: inset 0 1px 0 color-mix(in srgb, var(--horizon-haze) 70%, transparent);
	}
	.compact .sky {
		padding-block: 2.25rem 0.9rem;
	}
	.compact .sea {
		padding-block: 0.75rem 1.1rem;
	}
	.compact .frame {
		padding-inline: 1rem;
	}
	.compact .margined {
		grid-template-columns: minmax(0, 1fr);
	}
	.compact .main {
		grid-column: 1;
	}
	.compact .sun {
		width: calc(var(--sun-size) * 0.5);
		top: max(var(--sun-y), calc(var(--sun-size) * 0.25 + 0.4rem));
	}
</style>
