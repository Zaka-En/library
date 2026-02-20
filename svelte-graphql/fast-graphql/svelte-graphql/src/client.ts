// src/lib/houdini/client.ts
import { HoudiniClient, subscription } from '$houdini';
import { createClient } from 'graphql-ws';

//let refreshPromise: Promise<Response> | null = null;
// const pendingAuthRetries: (Promise<Response>)[] = [];
// type Resolver = (value: Response) => void
// const pendingAuthRetries: Resolver[] = []
// let isWaitingForReauth = false;
// const API_URL = 'http://localhost:8000/graphql';


// ESTA ES UN CHOARRADA QUE HA HECHO CLAUDE
// const customFetch: typeof fetch = async (input, init) => {
//     let response = await fetch(input, init)

//     if (response.status != 401) return response

//     if (!isWaitingForReauth) {
        
//         isWaitingForReauth = true

//         const refreshResult = await fetch(API_URL, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             credentials: 'include',
//             body: JSON.stringify({ query: `mutation RefreshToken { refreshToken { accessToken } }` })
//         });

//         isWaitingForReauth = false

//         if (refreshResult.ok) {
//             const retryResponse = await fetch(input, init)
            
//             const resolvers = [...pendingAuthRetries]
//             pendingAuthRetries.length = 0;
//             for(const resolve of resolvers){
//                 resolve(new Response()) // <--- Esta linea no sirve para nada
//             }

//             return retryResponse
//         }else{
//             pendingAuthRetries.length = 0
//             return refreshResult
//         }
//     }
    //     else {
    //         // Ya hay un refresh en curso, me encolo y espero
    //         const waitPromise = new Promise<Response>((resolve) => {
    //             pendingAuthRetries.push(resolve);
    //         });

    //         await waitPromise; // espero a que el primero termine el refresh

    //         // Cuando me despiertan, reintento mi petición original
    //         return fetch(input, init);
    //     }
    // };
// }

// const pendingAuthRetries: (Promise<Response>)[] = [];
// let isWaitingForReauth = false;

// const customFetch: typeof fetch = async (input, init) => {
//     // 1. Log inicial para confirmar que el fetch está entrando aquí
//     console.log("Houdini: Petición iniciada a", (input as Request).url || input);

//     let response = await fetch(input, init);

//     let isUnauthorized = false;

//     if (response.status == 401) { //  402 403
//         isUnauthorized = true;

//         try {
//             const responseBody = await response.json();
//             if (responseBody?.errors) {
//                 console.error(responseBody?.errors)
//             }
//         } catch {
//             // No es JSON, seguimos
//         }
//     } else {
//         return response;
//     }

//     // 4. --- LÓGICA DE REFRESH ---
//     if (isUnauthorized) {

//         if (!isWaitingForReauth) {
//             console.log("Houdini: Lanzando Silent Refresh...");
//             isWaitingForReauth = true;
//             const refreshResolt = await fetch(API_URL, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 credentials: 'include',
//                 body: JSON.stringify({
//                     query: `mutation RefreshToken { refreshToken { accessToken } }`
//                 })
//             });
//             if (refreshResolt.ok) {
//                 if (pendingAuthRetries.length) {
//                     Promise.all(pendingAuthRetries)
//                 }
//                 // haz ok
//             } else {
//                 //error en todos los promise
//             }
//         } else {
//             const waitingPromise = new Promise(() =)

//             pendingAuthRetries.push(waitingPromise)


//             try {
//                 const refreshResponse = await waitingPromise;

//                 if (refreshResponse?.ok) {
//                     console.log("Houdini: Refresh exitoso. Reintentando mutación original...");
//                     // Reintentamos la petición original
//                     return fetch(input, init);
//                 }
//             }
//             } catch (err) {
//             console.error("Houdini: Error crítico en el refresh", err);
//             return
//         }
//     }
// }

// return response;
// };




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

    }

    return response;
};

// const customFetch: typeof fetch = async (input, init) => {
//     // 1. Log inicial para confirmar que el fetch está entrando aquí
//     console.log("Houdini: Petición iniciada a", (input as Request).url || input);

//     let response = await fetch(input, init);

//     let isUnauthorized = false;

//     if (response.status == 401) { //  402 403
//         isUnauthorized = true;
        
//         try {
//             const responseBody = await response.json();
//             if (responseBody?.errors) {
//                 console.error(responseBody?.errors)
//             }
//         } catch {
//             // No es JSON, seguimos
//         }
//     } else {
//         return response;
//     }
        
//     // 4. --- LÓGICA DE REFRESH ---
//     if (isUnauthorized) {
//         console.warn("Houdini: Detectado error de Auth");

//         if (!isWaitingForReauth) {
//             console.log("Houdini: Lanzando Silent Refresh...");
//             isWaitingForReauth = true;
//             const refreshResolt = await fetch(API_URL, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 credentials: 'include',
//                 body: JSON.stringify({
//                     query: `mutation RefreshToken { refreshToken { accessToken } }`
//                 })
//             });
//             if (refreshResolt.ok) {
//                 if (pendingAuthRetries.length) {
//                     Promise.all(pendingAuthRetries)
//                 }
//                 // haz ok
//             } else {
//                 //error en todos los promise
//             }
//         } else {
//             const waitingPromise = new Promise(() =)

//             pendingAuthRetries.push(waitingPromise)
            
            
//             try {
//                 const refreshResponse = await waitingPromise;
    
//                 if (refreshResponse?.ok) {
//                         console.log("Houdini: Refresh exitoso. Reintentando mutación original...");
//                         // Reintentamos la petición original
//                         return fetch(input, init);
//                     }
//                 }
//             } catch (err) {
//                 console.error("Houdini: Error crítico en el refresh", err);
//                 return
//             }
//         }
//     }

//     return response;
// };

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