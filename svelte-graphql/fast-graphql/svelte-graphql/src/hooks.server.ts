import type { Handle } from '@sveltejs/kit';
import { authenticateUser, type UserPayLoad } from '$lib/server/auth';

const GRAPHQL_URL = 'http://localhost:8000/graphql'

export const handle: Handle = async ({ event, resolve }) => {
  let accessToken = event.cookies.get('access_token') as string;
  const refreshToken = event.cookies.get('refresh_token');
  let user: UserPayLoad | null = authenticateUser(accessToken);

  if (!user && refreshToken) {
    console.log("Token expirado en servidor. Intentando Refresh...");

    try {
      
      const response = await fetch(GRAPHQL_URL, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Cookie': `refresh_token=${refreshToken}`
         },
        
        body: JSON.stringify({
          query: `mutation RefreshToken { 
                    refreshToken { 
                        accessToken
                    } 
                  }`
        })
      });

      const result = await response.json();
      console.log("resultado de la petición de refresh", result)
      const newAccessToken = result.data?.refreshToken?.accessToken;

      if (newAccessToken) {
        console.log("Refresh exitoso en servidor.");

        
        event.cookies.set('access_token', newAccessToken, {
          path: '/',
          httpOnly: true,
          sameSite: 'strict',
          //secure: true
          maxAge: 15 * 60 // 15 min
        });

        
        accessToken = newAccessToken;

        user = authenticateUser(newAccessToken);
      } else {
        console.log("❌ Falló el refresh en servidor.");
      }
    } catch (error) {
      console.error("Error de red en refresh server:", error);
    }
  }

  event.locals.user = user;
  event.locals.token = accessToken;

  return await resolve(event);
};