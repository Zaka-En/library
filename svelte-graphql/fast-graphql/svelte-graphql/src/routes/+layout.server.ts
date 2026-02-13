import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = ({ locals }) =>{

  return{
    session: {
      user: locals.user,
      token: locals.token
    }
  }
}