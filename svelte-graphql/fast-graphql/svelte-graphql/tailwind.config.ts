import type { Config } from 'tailwindcss';

export default {
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'../comp-library/**/*.{svelte,js,ts,html}'],
	theme: {
		extend: {}
	},
	plugins: []
} satisfies Config;
