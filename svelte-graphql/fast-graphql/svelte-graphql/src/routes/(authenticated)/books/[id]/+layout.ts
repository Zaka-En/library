import type { LayoutLoad } from './$types';
import {graphql} from '$houdini'

const store = graphql(
    `
      query GetBook($id: Int!) {
        book(id: $id) {
        id title isbn publicationYear pages
        author { id name fullname country }
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