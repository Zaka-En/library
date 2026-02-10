import { HoudiniClient, subscription } from '$houdini';
import { createClient } from 'graphql-ws';

export default new HoudiniClient({
    url: 'http://localhost:8000/graphql',

    plugins: [
        subscription(() => createClient({
            url: 'ws://localhost:8000/graphql'
        }))
    ]

})
