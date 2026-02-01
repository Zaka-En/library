import { GET_BOOK } from "$lib/graphql/queries";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, fetch }) => {
  const { id } = params;

  const response = await fetch('http://backend:8000/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        query: `
          query GetBook($id: Int!) {
            book(id: $id) {
              id title isbn publicationYear pages
              author { id name }
            }
          }
        `,
        variables: { id: parseInt(id) }
      })
  });

  const result = await response.json();

  if (result.errors) {
    throw new Error(result.errors[0].message);
  }

  return {
    book: result.data.book
  };
};