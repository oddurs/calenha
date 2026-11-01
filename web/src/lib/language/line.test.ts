import { describe, expect, it } from 'vitest';
import { key, plain, stressSpans, tokenize } from './line';
import type { Entry } from './types';

const entry = (word: string, syllables: string[], stress: number) =>
	({ word, syllables, stress }) as Entry;

const lexicon = new Map([
	['miraluma', entry('miraluma', ['mi', 'ra', 'lu', 'ma'], 2)],
	['mirão', entry('mirão', ['mi', 'rão'], 1)],
	['lë', entry('lë', ['lë'], 0)]
]);

describe('key and plain', () => {
	it('folds capitals and breaths into the dictionary form', () => {
		expect(key('Miraluma')).toBe('miraluma');
		expect(key('mi·rão')).toBe('mirão');
	});
	it('drops accents for searching', () => {
		expect(plain('Célë')).toBe('cele');
	});
});

describe('tokenize', () => {
	it('reads words, breaths and punctuation', () => {
		const tokens = tokenize('lë Miraluma · mi·rão.', (k) => lexicon.get(k));
		expect(tokens.map((t) => t.kind)).toEqual(['word', 'word', 'breath', 'word']);
		const last = tokens[3];
		expect(last?.kind === 'word' && last.trail).toBe('.');
		expect(last?.kind === 'word' && last.aching).toBe(true);
		expect(last?.kind === 'word' && last.entry?.word).toBe('mirão');
	});
	it('leaves unknown words without an entry', () => {
		const [t] = tokenize('zuma', (k) => lexicon.get(k));
		expect(t?.kind === 'word' && t.entry).toBeUndefined();
	});
});

describe('stressSpans', () => {
	it('keeps capitals', () => {
		expect(stressSpans(lexicon.get('miraluma')!, 'Miraluma')).toEqual({
			before: 'Mira',
			stressed: 'lu',
			after: 'ma'
		});
	});
	it('keeps a breath inside the word', () => {
		expect(stressSpans(lexicon.get('mirão')!, 'mi·rão')).toEqual({
			before: 'mi·',
			stressed: 'rão',
			after: ''
		});
	});
	it('does not mark one-syllable words', () => {
		expect(stressSpans(lexicon.get('lë')!, 'lë').stressed).toBe('');
	});
});
