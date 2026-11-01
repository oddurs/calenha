import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/**
 * Every page is prerendered from the exported language data. Set BASE_PATH when the
 * site is served from a subfolder (GitHub Pages serves it from /calenha).
 *
 * @type {import('@sveltejs/kit').Config}
 */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({ fallback: '404.html', strict: true }),
		paths: { base: process.env.BASE_PATH ?? '' },
		prerender: { handleHttpError: 'fail', handleMissingId: 'fail' },
		alias: {
			$components: 'src/lib/components',
			$design: 'src/lib/design'
		}
	}
};

export default config;
