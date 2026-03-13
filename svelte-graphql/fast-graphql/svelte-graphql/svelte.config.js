import adapter from '@sveltejs/adapter-node';

const config = {
	kit: {
        adapter: adapter(),
        
        alias: {
            $houdini: ".houdini/"
        },

        csrf:{
			checkOrigin: false,
		}
        
    },
};

export default config;