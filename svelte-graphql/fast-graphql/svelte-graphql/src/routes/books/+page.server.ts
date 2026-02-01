import type { PageServerLoad } from "./$types";
import { GET_BOOKS } from "$lib/graphql/queries";
import { createClient } from "$lib/graphql/client";

export const load: PageServerLoad = async ({ fetch }) => {

  const client = createClient(fetch);

  const result = await client
    .query(GET_BOOKS, {})
    .toPromise()

  if (result.error) {
    console.error("GraphQL Error:", result.error);
    throw new Error(result.error.message);
  }

  return {
    books: result.data?.books ?? []
  }
}