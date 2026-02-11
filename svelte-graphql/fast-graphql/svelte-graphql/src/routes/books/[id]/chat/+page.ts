import type { PageLoad } from "./$types";
import { graphql } from "$houdini";

const bookChatSubStore = graphql(`
  subscription BookChat($bookId: Int!){
    bookChat(bookId: $bookId)
  }
`)


const sendBookChatMessageStore = graphql(`
  mutation SendBookChatMessage($bookId: Int!, $userName: String!, $message: String!) {
    sendBookChatMessage(bookId: $bookId, userName: $userName, message: $message)
  }
`)

export const load: PageLoad = async (event) => {
  const { store } = await event.parent(); 

  return {
    event,
    bookStore: store,
    bookChatSubStore,
    sendBookChatMessageStore
  }

}