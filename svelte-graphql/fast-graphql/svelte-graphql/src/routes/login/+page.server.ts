import { fail, redirect, type HttpError } from '@sveltejs/kit';
import type { Actions } from './$types';
import { graphql } from '$houdini';

const loginStore = graphql(
  `mutation Login($data: LoginInput!) {
    login(data: $data) {
      accessToken
      refreshToken
      tokenType
      user {
        email
        fullname
        id
        name
        rol
      }
    }
  }`
);

export const actions: Actions = {
  default: async (event) => {
    const data = await event.request.formData();
    const email = data.get('email') as string;
    const password = data.get('password') as string;


    console.log("ha entrado en el login ")

    let accessToken: string = ""
    let refreshToken: string = ""

    try {
      const respons = await fetch("http://api:8000/login",{
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        credentials: 'include',
        body: new URLSearchParams({
          "username": email,
          "password": password
        })
      })

      const datos = await respons.json()
      
      console.table(datos)


      accessToken = datos.access_token
      refreshToken = datos.refresh_token



    } catch (error) {
      console.error(error)
      
    }
 

    if (accessToken) {
      event.cookies.set('access_token', accessToken, {
        path: '/',
        httpOnly: true,
        //secure: true,
        sameSite: 'lax',
        maxAge: 60
      });
    }
      
    if(refreshToken){
      event.cookies.set('refresh_token', refreshToken, {
      path: '/',
      httpOnly: true,
      //secure: true,
      sameSite: 'strict',
      maxAge: 6 * 30 * 24 * 60 * 60
    });
    }
    
    if (accessToken) {
      throw redirect(303, event.url.searchParams.get("redirect") ?? "/books")
    }
    
  }
};