import type { PageServerLoad } from "../$types";
import { getContextClient } from "@urql/svelte";
import { GET_AUTHOR } from "$lib/graphql/queries";
import { client } from "$lib/graphql/client";



export const load: PageServerLoad = async ({ params }) => {



  const { id } = params

  const result = await client
    .query(GET_AUTHOR, { id: Number(id) }, { requestPolicy: 'network-only' })
    .toPromise()

  if (result.error) {
    throw new Error(result.error.message);
  }

  return {
    author: result.data?.author ?? null
  };
};