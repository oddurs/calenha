/**
 * Documentation for the design tokens. Values live only in tokens.css; this file
 * names and explains them so the /design page can show each one, live.
 */

export interface TokenDoc {
	name: string;
	note: string;
}

export const colours: { layer: string; tokens: TokenDoc[] }[] = [
	{
		layer: 'semantic',
		tokens: [
			{ name: '--color-page', note: 'the ground of every page — morning fog' },
			{ name: '--color-surface', note: 'a thicker fog, for fields and code' },
			{ name: '--color-ink', note: 'text — kelp' },
			{ name: '--color-ink-muted', note: 'secondary text — granite' },
			{ name: '--color-accent', note: 'headings and links — sea under cloud' },
			{ name: '--color-rule', note: 'hairlines — the horizon' },
			{ name: '--color-stress', note: 'the only bright thing: the stressed syllable' }
		]
	},
	{
		layer: 'primitive',
		tokens: [
			{ name: '--fog-50', note: '' },
			{ name: '--fog-100', note: '' },
			{ name: '--fog-200', note: '' },
			{ name: '--fog-300', note: '' },
			{ name: '--fog-400', note: '' },
			{ name: '--kelp-950', note: '' },
			{ name: '--kelp-900', note: '' },
			{ name: '--kelp-850', note: '' },
			{ name: '--kelp-800', note: '' },
			{ name: '--tide-600', note: '' },
			{ name: '--tide-300', note: '' },
			{ name: '--granite-600', note: '' },
			{ name: '--granite-300', note: '' },
			{ name: '--poppy-700', note: '' },
			{ name: '--poppy-400', note: '' }
		]
	}
];

export const typeScale: TokenDoc[] = [
	{ name: '--step-6', note: 'a word on its own page' },
	{ name: '--step-5', note: 'the opening line' },
	{ name: '--step-4', note: 'page titles' },
	{ name: '--step-3', note: '' },
	{ name: '--step-2', note: 'section headings, headwords' },
	{ name: '--step-1', note: 'lines of Calenha' },
	{ name: '--step-0', note: 'body' },
	{ name: '--step--1', note: 'notes and labels' },
	{ name: '--step--2', note: 'word-by-word glosses' }
];

export const space: TokenDoc[] = [
	{ name: '--space-3xs', note: '' },
	{ name: '--space-2xs', note: '' },
	{ name: '--space-xs', note: '' },
	{ name: '--space-s', note: '' },
	{ name: '--space-m', note: '' },
	{ name: '--space-l', note: '' },
	{ name: '--space-xl', note: '' },
	{ name: '--space-2xl', note: '' }
];

export const motion: TokenDoc[] = [
	{ name: '--duration-breath', note: 'how long a word takes to breathe in' },
	{ name: '--stagger-breath', note: 'the pause between words' },
	{ name: '--duration-quick', note: 'hover and press' },
	{ name: '--ease-tide', note: 'slow in, slower out' }
];
