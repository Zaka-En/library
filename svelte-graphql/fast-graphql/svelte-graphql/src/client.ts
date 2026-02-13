import { HoudiniClient, subscription } from '$houdini';
import { createClient } from 'graphql-ws';

export default new HoudiniClient({
    url: 'http://localhost:8000/graphql',
    fetchParams({ session }) {
        console.log('--- DEBUG HOUDINI CLIENT ---');
        console.log('Objeto session completo:', session);
        
        return {
            headers: {
                Authorization: session?.token ? `Bearer ${session.token}` : '',
            },
        }
    },
    plugins: [
        subscription(() => createClient({
            url: 'ws://localhost:8000/graphql',
        }))
    ]

})

