import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { graphql } from '$houdini';

const loginStore = graphql(
  `mutation Login($data: LoginInput!) {
    login(data: $data) {
      accessToken
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

  console.log('Respuesta Houdini:', JSON.stringify(response, null, 2));

  if (response.errors) {
    return fail(400, {error: response.errors[0].message})
  }

  const token = response.data?.login.accessToken;

  if (token) {
    event.cookies.set('access_token',token, {
      path: '/',
      httpOnly: true,
      sameSite: 'strict',
      maxAge: 60 * 60 * 24
    });

    throw redirect(303, 'authors');
  }

    return fail(400,{ error: 'Login fallido' })
  }
};