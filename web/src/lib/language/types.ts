/**
 * The data contract, as written by `calenha export` (src/calenha/export.py).
 * The Python side owns the rules; this side only presents what they produced.
 * Change both together, and bump SCHEMA when the shape changes.
 */

export const SCHEMA = 1;

export type PartOfSpeech =
	'noun' | 'verb' | 'adjective' | 'name' | 'particle' | 'pronoun' | 'number';

/** How a word is said: its syllables, which one carries the stress, and IPA. */
export interface Shape {
	syllables: string[];
	stress: number;
	ipa: string;
}

export interface Part {
	form: string;
	meaning: string;
	kind: 'root' | 'affix' | 'word';
	/** a root slug or an entry slug, when the part has a page of its own */
	target: string | null;
}

export interface Step {
	form: string;
	change: string;
	index: number;
}

export interface Entry extends Shape {
	slug: string;
	word: string;
	gloss: string;
	/** the gloss cut to its first sense, for word-by-word reading */
	short: string;
	pos: PartOfSpeech;
	label: string;
	domain: string;
	sense: string | null;
	parts: Part[];
	old: string | null;
	history: Step[];
	family: string[];
	/** indexes into Language.phrases */
	phrases: number[];
	/** slugs of texts that use the word */
	texts: string[];
}

export interface Root {
	root: string;
	slug: string;
	meaning: string;
	kin: string | null;
	children: string[];
}

export interface Affix {
	form: string;
	meaning: string;
	makes: string;
	examples: string[];
}

export interface Phrase {
	text: string;
	literal: string;
	translation: string;
	topic: string;
	featured: boolean;
}

export interface TextLine {
	text: string;
	translation: string;
}

export interface Text {
	slug: string;
	title: string;
	english: string;
	kind: string;
	/** trusted HTML, rendered from the language's own markdown */
	note: string;
	/** an empty `text` marks a stanza break */
	lines: TextLine[];
}

export interface Change {
	index: number;
	name: string;
	rule: [string, string][];
	when: string;
	environment: string;
	/** trusted HTML */
	note: string;
	shaped: string[];
}

export interface Candidate extends Shape {
	text: string;
	echoes: string[];
}

export interface Doc {
	title: string;
	lede: string;
	/** trusted HTML */
	html: string;
}

export interface Language {
	schema: number;
	meta: {
		version: string;
		built: string;
		counts: Record<string, number>;
	};
	domains: { name: string; intro: string }[];
	topics: string[];
	entries: Entry[];
	roots: Root[];
	affixes: Affix[];
	phrases: Phrase[];
	texts: Text[];
	changes: Change[];
	unspoken: { things: Candidate[]; invitations: Candidate[] };
	docs: Record<'grammar' | 'sounds' | 'world' | 'principles', Doc>;
}
