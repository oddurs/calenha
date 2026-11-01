/**
 * The site's structure: four sections, each with its pages. Every page is named
 * twice — in Calenha, which titles the page, and in English, which navigates.
 */

import { resolve } from '$app/paths';

export interface PageInfo {
	path: string;
	english: string;
	/** a word from the lexicon */
	calenha: string;
}

export interface SectionInfo {
	english: string;
	calenha: string;
	pages: PageInfo[];
}

export const sections: SectionInfo[] = [
	{
		english: 'dictionary',
		calenha: 'palaura',
		pages: [
			{ path: '/words', english: 'words', calenha: 'palaura' },
			{ path: '/roots', english: 'roots', calenha: 'raízë' },
			{ path: '/unspoken', english: 'unspoken', calenha: 'semë' }
		]
	},
	{
		english: 'language',
		calenha: 'como',
		pages: [
			{ path: '/grammar', english: 'grammar', calenha: 'como' },
			{ path: '/sounds', english: 'sounds', calenha: 'vozë' },
			{ path: '/history', english: 'history', calenha: 'vaza' }
		]
	},
	{
		english: 'reading',
		calenha: 'lenda',
		pages: [
			{ path: '/texts', english: 'texts', calenha: 'lenda' },
			{ path: '/phrases', english: 'phrases', calenha: 'fala' },
			{ path: '/reader', english: 'reader', calenha: 'olhu' }
		]
	},
	{
		english: 'world',
		calenha: 'solmara',
		pages: [
			{ path: '/world', english: 'Solmara', calenha: 'solmara' },
			{ path: '/principles', english: 'principles', calenha: 'calma' },
			{ path: '/design', english: 'design', calenha: 'fazu' }
		]
	}
];

/** The section a path belongs to, if any. Word pages belong to the dictionary. */
export function sectionOf(pathname: string, base: string): SectionInfo | undefined {
	const path = pathname.slice(base.length) || '/';
	const route = path.startsWith('/words/') ? '/words' : path.replace(/^\/texts\/.+/, '/texts');
	return sections.find((s) => s.pages.some((p) => p.path === route));
}

export const href = (path: string) => resolve(path as '/');
