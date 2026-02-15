import type { PageLoad } from './$types';
import { graphql, GetAllAuthorsStore } from '$houdini';

// 1. Definimos la query fuera del load para que Houdini la procese
/* const GetAllAuthorsStore = graphql(`
  query GetAllAuthors($first: Int) {
    authors(first: $first) @list(name: "All_Authors") @paginate(mode: Infinite){
      edges {
        node {
          id
          name
          biography
          country
          fullname
        }
      }
      pageInfo {
        totalCount
        hasNextPage
        endCursor
      }
    }
  }
`); */

export const load: PageLoad = async (event) => {
   
  const store = new GetAllAuthorsStore()
  await store.fetch({
    event,
    variables: { first: 10 }
  });

    

    return {
      GetAuthors: store
    };
};