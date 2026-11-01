import { error } from '@sveltejs/kit';
import { language, text } from '$lib/language';
import type { EntryGenerator, PageLoad } from './$types';

export const entries: EntryGenerator = () => language.texts.map(({ slug }) => ({ slug }));

export const load: PageLoad = ({ params }) => {
	const found = text(params.slug);
	if (!found) error(404, `No text lives at ${params.slug}`);
	return {
		text: found,
		others: language.texts.filter((t) => t.slug !== found.slug)
	};
};
