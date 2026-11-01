/** Addresses for the site's pages, base path included. */

import { resolve } from '$app/paths';

export const wordHref = (slug: string) => resolve('/words/[slug]', { slug });
export const textHref = (slug: string) => resolve('/texts/[slug]', { slug });
export const rootHref = (slug: string) => `${resolve('/roots')}#r-${slug}`;
export const changeHref = (index: number) => `${resolve('/history')}#c-${index}`;
