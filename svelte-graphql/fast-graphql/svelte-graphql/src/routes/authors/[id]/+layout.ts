import type { LayoutLoad } from './$types';
import {graphql} from '$houdini'

const store = graphql(
    `
      query GetAuthor($id: Int!) {
      author (id: $id) { 
        id name fullname biography country 
        books { id title publicationYear  pages}
      }
    }
    `
  )

export const load: LayoutLoad = async ( event ) => {
	
  const id = Number(event.params.id)

  await store.fetch({
    event,
    variables: {
      id
    }
  })

	return { store };
};