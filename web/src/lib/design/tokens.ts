/**
 * Documentation for the design tokens. Values live only in tokens.css; this file
 * names and explains them so /design can show each one, live.
 */

export interface TokenDoc {
	name: string;
	note: string;
}

/** semantic colour roles — each hour sets every one of them */
export const roles: TokenDoc[] = [
	{ name: '--color-page', note: 'the ground of every page' },
	{ name: '--color-surface', note: 'fields, code, the footer' },
	{ name: '--color-ink', note: 'text' },
	{ name: '--color-ink-muted', note: 'notes, labels, glosses' },
	{ name: '--color-accent', note: 'the current place, letters, roots' },
	{ name: '--color-rule', note: 'hairlines' },
	{ name: '--color-beat', note: 'the stressed syllable, and nothing else' },
	{ name: '--color-sky', note: 'above the horizon' },
	{ name: '--color-haze', note: 'light gathered at the horizon' },
	{ name: '--color-sea', note: 'below the horizon' }
];

export const primitives: { family: string; note: string; tokens: string[] }[] = [
	{
		family: 'fog',
		note: 'the marine layer',
		tokens: ['--fog-50', '--fog-100', '--fog-200', '--fog-300', '--fog-400']
	},
	{
		family: 'pacific',
		note: 'the sea in its depths',
		tokens: [
			'--pacific-200',
			'--pacific-450',
			'--pacific-500',
			'--pacific-600',
			'--pacific-650',
			'--pacific-800',
			'--pacific-850',
			'--pacific-900',
			'--pacific-950'
		]
	},
	{
		family: 'sage',
		note: 'the grey scrub of the dry hills',
		tokens: ['--sage-100', '--sage-200', '--sage-300', '--sage-700', '--sage-900']
	},
	{
		family: 'rose',
		note: 'first light',
		tokens: ['--rose-100', '--rose-200', '--rose-300', '--rose-400']
	},
	{
		family: 'amber',
		note: 'the golden hour',
		tokens: [
			'--amber-100',
			'--amber-200',
			'--amber-300',
			'--amber-400',
			'--amber-500',
			'--amber-900'
		]
	},
	{
		family: 'poppy',
		note: 'the only bright thing',
		tokens: ['--poppy-300', '--poppy-600', '--poppy-700']
	}
];

export const typeScale: TokenDoc[] = [
	{ name: '--step-6', note: 'a word on its own page' },
	{ name: '--step-5', note: 'the opening line; page titles' },
	{ name: '--step-4', note: 'Calenha only, in a text' },
	{ name: '--step-3', note: 'headwords' },
	{ name: '--step-2', note: 'lines of Calenha' },
	{ name: '--step-1', note: 'ledes, meanings' },
	{ name: '--step-0', note: 'body' },
	{ name: '--step--1', note: 'notes, glosses, labels' }
];

export const space: TokenDoc[] = [
	{ name: '--space-3xs', note: '' },
	{ name: '--space-2xs', note: '' },
	{ name: '--space-xs', note: '' },
	{ name: '--space-s', note: '' },
	{ name: '--space-m', note: '' },
	{ name: '--space-l', note: 'the gap beside the margin column' },
	{ name: '--space-xl', note: 'between sections' },
	{ name: '--space-2xl', note: '' }
];

export const motion: TokenDoc[] = [
	{ name: '--duration-breath', note: 'how long a word takes to arrive' },
	{ name: '--stagger-breath', note: 'the pause between words' },
	{ name: '--duration-quick', note: 'hover and press' },
	{ name: '--ease-tide', note: 'slow in, slower out' }
];
