/**
 * Reading a line of Calenha: split it into words, breaths and punctuation, and find
 * where each word's stress falls in the letters as written (capitals and mid-word
 * breaths included). No phonology lives here — stress comes from the exported data.
 */

import type { Entry, Shape } from './types';

export const BREATH = '·';
const PUNCTUATION = /^([.,;:!?"'—–]*)(.*?)([.,;:!?"'—–]*)$/u;

export type Token =
	| { kind: 'breath' }
	| {
			kind: 'word';
			/** the word as written, without surrounding punctuation */
			shown: string;
			/** the dictionary form: lowercase, composed, no breath */
			key: string;
			lead: string;
			trail: string;
			/** broken by a breath: the word aches */
			aching: boolean;
			entry: Entry | undefined;
	  };

/** The dictionary form of a written word. */
export function key(word: string): string {
	return word.normalize('NFC').toLowerCase().split(BREATH).join('');
}

/** Accents removed, for searching and sorting: célë → cele. */
export function plain(text: string): string {
	return text.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
}

export function tokenize(line: string, lookup: (key: string) => Entry | undefined): Token[] {
	const tokens: Token[] = [];
	for (const raw of line.trim().split(/\s+/u)) {
		if (!raw) continue;
		if (raw === BREATH) {
			tokens.push({ kind: 'breath' });
			continue;
		}
		const [, lead = '', shown = '', trail = ''] = PUNCTUATION.exec(raw) ?? [];
		const k = key(shown);
		if (!k) continue;
		tokens.push({
			kind: 'word',
			shown,
			key: k,
			lead,
			trail,
			aching: shown.includes(BREATH),
			entry: lookup(k)
		});
	}
	return tokens;
}

export interface Spans {
	before: string;
	stressed: string;
	after: string;
}

/**
 * Split a written word around its stressed syllable. `shown` may differ from the
 * dictionary form by capitals and breath marks; both are kept. One-syllable words
 * carry no mark, so everything is returned in `before`.
 */
export function stressSpans(shape: Pick<Shape, 'syllables' | 'stress'>, shown: string): Spans {
	const letters = [...shown];
	const positions = letters.flatMap((ch, i) => (ch === BREATH ? [] : [i]));
	const plainLength = shape.syllables.reduce((n, s) => n + [...s].length, 0);
	if (shape.syllables.length < 2 || positions.length !== plainLength) {
		return { before: shown, stressed: '', after: '' };
	}
	const start = shape.syllables.slice(0, shape.stress).reduce((n, s) => n + [...s].length, 0);
	const end = start + [...(shape.syllables[shape.stress] ?? '')].length;
	const a = positions[start] ?? 0;
	const b = (positions[end - 1] ?? 0) + 1;
	return {
		before: letters.slice(0, a).join(''),
		stressed: letters.slice(a, b).join(''),
		after: letters.slice(b).join('')
	};
}
