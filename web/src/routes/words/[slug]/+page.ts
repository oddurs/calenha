import { error } from '@sveltejs/kit';
import { entry, language } from '$lib/language';
import type { EntryGenerator, PageLoad } from './$types';

export const entries: EntryGenerator = () => language.entries.map(({ slug }) => ({ slug }));

export const load: PageLoad = ({ params }) => {
	const found = entry(params.slug);
	if (!found) error(404, `No word lives at ${params.slug}`);
	const i = language.entries.indexOf(found);
	return {
		entry: found,
		before: language.entries[i - 1],
		after: language.entries[i + 1]
	};
};
