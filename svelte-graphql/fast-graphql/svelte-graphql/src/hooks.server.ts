import type { Handle } from '@sveltejs/kit';
import { setSession } from '$houdini'; // ← IMPORTANTE: importar setSession
import { authenticateUser } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('access_token') as string;
  const user = authenticateUser(token);
  
  // ← Aquí está la clave: usar setSession de Houdini
  setSession(event, { 
    user,
    token 
  });
  
  // Opcional: también puedes mantenerlo en locals si lo necesitas para SvelteKit
  event.locals.user = user;
  event.locals.token = token;
  
  return await resolve(event);
};