import type { PageLoad } from "./$types"
import { graphql } from '$houdini'



const authorNamesStore = graphql(`
  query GetAuthorNamesWithId{
    authorsQuery{
      id
      name
    }
  }
`)

export const load: PageLoad = async (event) => {

  await authorNamesStore.fetch({ event })

  return {
    authorNamesStore
  }
}