// src/lib/houdini/client.ts
import { HoudiniClient, subscription } from '$houdini';
import { createClient } from 'graphql-ws';
import { browser } from '$app/environment';

const API_URL = 'http://localhost:8000/graphql';
let refreshPromise: Promise<Response> | null = null;

const customFetch: typeof fetch = async (input, init) => {
    // 1. Log inicial para confirmar que el fetch está entrando aquí
    console.log("Houdini: Petición iniciada a", (input as Request).url || input);

    let response = await fetch(input, init);

    // 2. Analizar la respuesta ANTES de darla por buena
    let isUnauthorized = false;
    let responseBody: any = null;

    if (response.status === 401) {
        isUnauthorized = true;
    } else {
        // Clonamos para inspeccionar el JSON por si hay errores GraphQL
        const clone = response.clone();
        try {
            responseBody = await clone.json();
            if (responseBody?.errors) {
                isUnauthorized = responseBody.errors.some(
                    (e: any) => e.message === 'Token expired' || 
                                e.extensions?.code === 'UNAUTHENTICATED' ||
                                e.message.includes("not authenticated") // Ajusta según tu backend
                );
                if (isUnauthorized) console.warn("Houdini: Detectado error de Auth en 200 OK");
            }
        } catch {
            // No es JSON, seguimos
        }
    }

    // 3. Si NO es un error de auth y la respuesta es ok, la devolvemos ahora sí
    if (!isUnauthorized && response.ok) {
        return response;
    }

    // 4. --- LÓGICA DE REFRESH ---
    if (isUnauthorized) {
        if (!refreshPromise) {
            console.log("Houdini: Lanzando Silent Refresh...");
            refreshPromise = fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    query: `mutation RefreshToken { refreshToken { accessToken } }`
                })
            });
        }

        try {
            const refreshResponse = await refreshPromise;
            refreshPromise = null; 

            if (refreshResponse.ok) {
                const refreshJson = await refreshResponse.json();
                if (refreshJson.data?.refreshToken?.accessToken) {
                    console.log("Houdini: Refresh exitoso. Reintentando mutación original...");
                    // Reintentamos la petición original
                    return fetch(input, init);
                }
            }
        } catch (err) {
            console.error("Houdini: Error crítico en el refresh", err);
        }

        // Si llegamos aquí, el refresh falló
        if (browser) {
            console.error("Houdini: Sesión expirada. Redirigiendo...");
            window.location.href = '/login?expired=true';
        }
    }

    return response;
};

export default new HoudiniClient({
    url: API_URL,
    fetchParams() {
        return { credentials: 'include' };
    },
    
    plugins: [
        () => ({
            network: async (ctx, { next }) => {
                
                ctx.fetch = customFetch;
                return next(ctx);
            }
        }),
        subscription(() => createClient({
            url: 'ws://localhost:8000/graphql'
        }))
    ]
});