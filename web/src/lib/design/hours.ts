/**
 * The page keeps Calenha time. Instead of light and dark, the site has hours —
 * each a set of semantic colour tokens in tokens.css, selected by `data-hour`.
 *
 * Following the sun (the default), the hour comes from the viewer's local clock.
 * A system preference for dark always means night. Anyone may choose an hour;
 * the choice is remembered in their browser only.
 */

export const HOURS = ['alva', 'nevoa', 'tarde', 'solouro', 'noite'] as const;
export type Hour = (typeof HOURS)[number];
export type HourChoice = Hour | 'sun';

export const STORAGE_KEY = 'calenha:hour';

export const hourInfo: Record<Hour, { word: string; english: string; note: string }> = {
	alva: {
		word: 'alva',
		english: 'dawn',
		note: 'first light; the sky blushes, the sea is still grey'
	},
	nevoa: { word: 'nevoã', english: 'morning fog', note: 'the marine layer, greeted like a guest' },
	tarde: {
		word: 'tardë',
		english: 'afternoon',
		note: 'warm stone, cool air; the hour the language was made for'
	},
	solouro: {
		word: 'solouro',
		english: 'golden hour',
		note: 'sun-gold; the hour everyone stops for'
	},
	noite: { word: 'noitë', english: 'night', note: 'the sea and the sky become one dark' }
};

/**
 * Which hour to show. Must stay self-contained (no references outside its body):
 * its source is inlined into every page so the hour is set before first paint.
 */
export function pickHour(choice: string | null, localHour: number, prefersDark: boolean): Hour {
	const known = ['alva', 'nevoa', 'tarde', 'solouro', 'noite'];
	if (choice && known.includes(choice)) return choice as Hour;
	if (prefersDark) return 'noite';
	if (localHour >= 5 && localHour < 9) return 'alva';
	if (localHour >= 9 && localHour < 13) return 'nevoa';
	if (localHour >= 13 && localHour < 17) return 'tarde';
	if (localHour >= 17 && localHour < 20) return 'solouro';
	// a viewer who prefers light is not plunged into night; the fog holds
	return 'nevoa';
}

/** The inline script for app.html: reads the choice, sets `data-hour` on <html>. */
export const hourScript = `(function(){try{var pick=${pickHour.toString()};var c=null;try{c=localStorage.getItem(${JSON.stringify(
	STORAGE_KEY
)})}catch(e){}var d=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches;document.documentElement.dataset.hour=pick(c,new Date().getHours(),d);document.documentElement.dataset.hourChoice=c||'sun'}catch(e){}})();`;
