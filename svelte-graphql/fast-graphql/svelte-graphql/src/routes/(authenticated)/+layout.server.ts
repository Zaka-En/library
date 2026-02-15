import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = ({ locals, url }) => {
  
  console.log(locals.user)
  if (!locals.user) {
    throw redirect(303, `/login?redirect=${url.pathname}`);
  }


  return {
    user: locals.user
  };
};