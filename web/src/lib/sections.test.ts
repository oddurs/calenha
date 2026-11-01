import { describe, expect, it, vi } from 'vitest';

vi.mock('$app/paths', () => ({ resolve: (p: string) => p }));

const { sectionOf, sections } = await import('./sections');
const lexicon = (await import('$lib/data/language.json')).default as {
	entries: { word: string }[];
};

describe('sections', () => {
	it('finds the section of a page, a word and a text', () => {
		expect(sectionOf('/roots', '')?.english).toBe('dictionary');
		expect(sectionOf('/calenha/words/thalire', '/calenha')?.english).toBe('dictionary');
		expect(sectionOf('/texts/nevoa', '')?.english).toBe('reading');
		expect(sectionOf('/', '')).toBeUndefined();
	});

	it('names every page with a real Calenha word', () => {
		const words = new Set(lexicon.entries.map((e) => e.word));
		for (const s of sections) for (const p of s.pages) expect(words).toContain(p.calenha);
	});
});
