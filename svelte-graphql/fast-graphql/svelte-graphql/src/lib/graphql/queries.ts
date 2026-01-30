import { gql } from "@urql/svelte";

export const GET_AUTHORS = gql`
  query GetAuthors {
    authors { id name country }
  }
`;

export const GET_AUTHOR = gql`
  query GetAuthor($id: Int!) {
    author(id: $id) { 
      id name fullname biography country 
      books { id title publicationYear  pages}
    }
  }
`;


export const GET_BOOKS = gql`
  query GetBooks {
    books {
      id title isbn publicationYear pages
      author { id name }
    }
  }
`;

export const GET_BOOK = gql`
  query GetBook($id: Int!) {
    book(id: $id) {
      id title isbn publicationYear pages
      author { id name country }
    }
  }
`;

export const MY_READING_PROGRESS = gql`
  query MyReadingProgress($userId: String!) {
    myReadingProgress(userId: $userId) {
      id currentPage startDate
      book {
        id title pages
        author { name }
      }
    }
  }
`;




