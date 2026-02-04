import { graphql } from "$houdini";
import type { PageLoad } from "./$types";

const store = graphql(`
  query GetBooks {
    books {
      id title isbn publicationYear pages
      author { id name }
    }
  }
`)

export const load: PageLoad = async (event) => {

  await store.fetch({
    event
  })


  return {
    store
  }
  
}