import type { PageLoad } from './$types';
import { graphql } from '$houdini';

const authorsStore = graphql(`
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
`); 

export const load: PageLoad = async (event) => {
   
 
  await authorsStore.fetch({
    event,
    variables: { first: 10 }
  });

    

  return {
    authorsStore
  };
};