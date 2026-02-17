// src/lib/houdini/client.ts
import { HoudiniClient, subscription } from '$houdini';
import { createClient } from 'graphql-ws';

const API_URL = 'http://localhost:8000/graphql';
//let refreshPromise: Promise<Response> | null = null;
const pendingAuthRetries: (Promise<Response>)[] = [];
let isWaitingForReauth = false;

const customFetch: typeof fetch = async (input, init) => {
    // 1. Log inicial para confirmar que el fetch está entrando aquí
    console.log("Houdini: Petición iniciada a", (input as Request).url || input);

    let response = await fetch(input, init);

    let isUnauthorized = false;

    if (response.status == 401) { //  402 403
        isUnauthorized = true;
        
        try {
            const responseBody = await response.json();
            if (responseBody?.errors) {
                console.error(responseBody?.errors)
            }
        } catch {
            // No es JSON, seguimos
        }
    } else {
        return response;
    }
        
    // 4. --- LÓGICA DE REFRESH ---
    if (isUnauthorized) {
        console.warn("Houdini: Detectado error de Auth");

        if (!isWaitingForReauth) {
            console.log("Houdini: Lanzando Silent Refresh...");
            isWaitingForReauth = true;
            const refreshResolt = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    query: `mutation RefreshToken { refreshToken { accessToken } }`
                })
            });
            if (refreshResolt.ok) {
                if (pendingAuthRetries.length) {
                    Promise.all(pendingAuthRetries)
                }
                // haz ok
            } else {
                //error en todos los promise
            }
        } else {
            const waitingPromise = new Promise(() =)

            pendingAuthRetries.push(waitingPromise)
            
            
            try {
                const refreshResponse = await waitingPromise;
    
                if (refreshResponse?.ok) {
                        console.log("Houdini: Refresh exitoso. Reintentando mutación original...");
                        // Reintentamos la petición original
                        return fetch(input, init);
                    }
                }
            } catch (err) {
                console.error("Houdini: Error crítico en el refresh", err);
                return
            }
        }
    }

    return response;
};

export default new HoudiniClient({
    url: API_URL,
    fetchParams() {
        return { credentials: 'include' };
    },
    
    //houdini functions/plugins pipeline
    plugins: [
        () => ({
            network: async (ctx, { next }) => {
                
                ctx.fetch = customFetch;
                return next(ctx);
            },
        }),
        subscription(() => createClient({
            url: 'ws://localhost:8000/graphql'
        }))
    ]
});