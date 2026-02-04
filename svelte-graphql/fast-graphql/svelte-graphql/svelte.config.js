import adapter from '@sveltejs/adapter-node';

const config = {
	kit: {
        adapter: adapter(),

        alias: {
            $houdini: ".houdini/"
        }
    }
};

export default config;