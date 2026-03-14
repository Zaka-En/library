import { redirect, type Handle, type HandleFetch } from '@sveltejs/kit';
import { authenticateUser, getUserfromPayLoad, type UserPayLoad } from '$lib/server/auth';
import { PUBLIC_INTERNAL_API_URL } from '$env/static/public';

const GRAPHQL_URL = 'http://api:8000/graphql'

export const handle: Handle = async ({ event, resolve }) => {
  let accessToken = event.cookies.get('access_token') as string;
  const refreshToken = event.cookies.get('refresh_token') as string;
  let isAuthenticated = accessToken ? authenticateUser(accessToken) : false;


  let user: UserPayLoad | null = accessToken ? getUserfromPayLoad(accessToken) : null;

  console.log("===============================================")
  console.log("user in hooks:", user)
  console.log("===============================================")



  event.locals.user = user;
  event.locals.isAuthenticated = isAuthenticated
  event.locals.token = accessToken;

  return await resolve(event, {
    filterSerializedResponseHeaders: (name) => name === "content-type",
  });
};

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {

  console.log("===============================================")
  console.log("INTERCEPTING THE FETCH REQUEST FROM SVELTEKIT")
  console.log(`access_token=${event.cookies.get("access_token") ?? "BlaBla"}`);  
  console.log("===============================================")
  const res = await fetch(request,{
    headers: {
      ...Object.fromEntries(request.headers),
      Cookie: `access_token=${event.cookies.get("access_token") ?? ""}`,
    }
  })

  if (res.status === 401 || res.status === 403) {

    const error = await res.clone().json()
    const errorMsg = error.errors[0].message as string
    let failedRefresh: boolean = false

    if (errorMsg === "ACCESS_TOKEN_EXPIRED") {
      const r = await fetch(`${PUBLIC_INTERNAL_API_URL.replace("/graphql", "")}/refresh`, {
        method: 'POST',
        headers: {          
          Cookie: `refresh_token=${event.cookies.get("refresh_token") ?? ""}`
        }
      })

      

      console.log("===============================================")
      console.log("RETRYING REFRESH")
      console.log("===============================================")

      if (r.ok) {
        const setCookieHeader = r.headers.get('set-cookie') ?? ""
        const match = setCookieHeader.match(/access_token=([^;]+)/);
        if (match?.[1]) {
          event.cookies.set('access_token', match[1], {
            path: '/',
            httpOnly: true,
            sameSite: 'strict',
            secure: false, // true en producción con HTTPS
          });
        }

        console.log("===============================================")
        console.log("IT HAS BEEN REFRESHED CORRECTLY")
        console.log("===============================================")

        return fetch(new Request(request ,{
          ...Object.fromEntries(request.headers),
          headers: {          
            Cookie: `access_token=${event.cookies.get("access_token") ?? ""}`
          }
        }))
      }

      failedRefresh = true
    }

    if (errorMsg !== "ACCESS_TOKEN_EXPIRED" || failedRefresh) {
      throw redirect(303, `/login`);
    }

  }

  return res
}