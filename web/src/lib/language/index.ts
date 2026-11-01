/**
 * The language, loaded once from the exported data, with the lookups pages need.
 */

import raw from '$lib/data/language.json';
import { key, tokenize } from './line';
import type { Entry, Language, Root, Text } from './types';
import { SCHEMA } from './types';

export const language = raw as unknown as Language;

if (language.schema !== SCHEMA) {
	throw new Error(
		`language.json has schema ${language.schema}, the site expects ${SCHEMA}. Run \`npm run data\`.`
	);
}

const bySlug = new Map(language.entries.map((e) => [e.slug, e]));
const byWord = new Map<string, Entry>();
for (const e of language.entries) if (!byWord.has(e.word)) byWord.set(e.word, e);
const roots = new Map(language.roots.map((r) => [r.slug, r]));
const texts = new Map(language.texts.map((t) => [t.slug, t]));

export const entry = (slug: string): Entry | undefined => bySlug.get(slug);
export const lookup = (word: string): Entry | undefined => byWord.get(key(word));
export const root = (slug: string): Root | undefined => roots.get(slug);
export const text = (slug: string): Text | undefined => texts.get(slug);
export const read = (line: string) => tokenize(line, lookup);

export const featured = language.phrases.find((p) => p.featured) ??
	language.phrases[0] ?? { text: '', translation: '' };

export * from './line';
export type * from './types';
