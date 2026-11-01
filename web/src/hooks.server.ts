import type { Handle } from '@sveltejs/kit';
import { hourScript } from '$design/hours';

// set the hour before first paint, so the sky never flashes the wrong colour
export const handle: Handle = ({ event, resolve }) =>
	resolve(event, {
		transformPageChunk: ({ html }) => html.replace('%calenha.hour%', hourScript)
	});
