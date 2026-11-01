import { describe, expect, it } from 'vitest';
import { hourScript, pickHour } from './hours';

describe('pickHour', () => {
	it('follows the sun through the day', () => {
		expect(pickHour(null, 6, false)).toBe('alva');
		expect(pickHour(null, 10, false)).toBe('nevoa');
		expect(pickHour(null, 15, false)).toBe('tarde');
		expect(pickHour(null, 18, false)).toBe('solouro');
	});
	it('keeps the fog at night for those who prefer light', () => {
		expect(pickHour(null, 23, false)).toBe('nevoa');
	});
	it('is always night for those who prefer dark', () => {
		expect(pickHour(null, 12, true)).toBe('noite');
	});
	it('honours a chosen hour over everything', () => {
		expect(pickHour('solouro', 3, true)).toBe('solouro');
	});
	it('ignores choices it does not know', () => {
		expect(pickHour('midnight', 10, false)).toBe('nevoa');
	});
});

describe('hourScript', () => {
	it('is a self-contained script that sets the hour', () => {
		const root = { dataset: {} as Record<string, string> };
		const run = new Function('document', 'window', 'localStorage', 'matchMedia', hourScript);
		const media = () => ({ matches: false });
		run({ documentElement: root }, { matchMedia: media }, { getItem: () => 'tarde' }, media);
		expect(root.dataset.hour).toBe('tarde');
		expect(root.dataset.hourChoice).toBe('tarde');
	});
});
