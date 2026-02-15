import { fail, redirect } from '@sveltejs/kit';
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


    const response = await loginStore.mutate(
      { data: { email, password } },
      { event } 
    );

    

    if (response.errors) {
      return fail(401, {error: response.errors[0].message})
    }

    const accessToken = response.data?.login.accessToken;
    const refreshToken = response.data?.login.refreshToken;

    if (accessToken) {
      event.cookies.set('access_token', accessToken, {
        path: '/',
        httpOnly: true,
        //secure: true,
        sameSite: 'lax',
        maxAge: 15 * 60
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
    
    
    throw redirect(303, event.url.searchParams.get("redirect") ?? "/books")

    
  }
};