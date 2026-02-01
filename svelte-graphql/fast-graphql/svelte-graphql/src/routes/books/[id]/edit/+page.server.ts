import { GET_BOOK, GET_AUTHORS } from "$lib/graphql/queries";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, fetch }) => {
  const { id } = params;
  
  // Fetch book details
  const bookResponse = await fetch('http://backend:8000/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: GET_BOOK.loc?.source.body || GET_BOOK,
      variables: { id: parseInt(id) }
    })
  });

  // Fetch authors for the dropdown
  const authorsResponse = await fetch('http://backend:8000/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: GET_AUTHORS.loc?.source.body || GET_AUTHORS
    })
  });

  const bookResult = await bookResponse.json();
  const authorsResult = await authorsResponse.json();
  
  if (bookResult.errors) {
    throw new Error(bookResult.errors[0].message);
  }

  if (authorsResult.errors) {
    throw new Error(authorsResult.errors[0].message);
  }

  return {
    book: bookResult.data.book,
    authors: authorsResult.data.authors
  };
};