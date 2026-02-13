
import type { PageLoad } from './$types';
import {graphql} from "$houdini"
import { load_GetAuthors } from '$houdini';



export const load: PageLoad = async (event) => {

  return{
    ...(await load_GetAuthors({ 
        event, 
        variables: { first: 10 } 
    }))
  }
};