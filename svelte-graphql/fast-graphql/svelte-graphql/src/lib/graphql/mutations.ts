import { gql } from '@urql/svelte';

export const CREATE_AUTHOR = gql`
  mutation CreateAuthor($input: CreateAuthorInput!) {
    createAuthor(input: $input) { id name  }
  }
`;

export const UPDATE_AUTHOR = gql`
  mutation UpdateAuthor($input: UpdateAuthorInput!) {
    updateAuthor(input: $input) { id name biography country }
  }
`;

export const CREATE_BOOK = gql`
  mutation CreateBook($input: CreateBookInput!) {
    createBook(input: $input) { id title }
  }
`;

export const START_READING = gql`
  mutation StartReading($input: StartReadingInput!) {
    startReading(input: $input) { id currentPage startDate }
  }
`;

export const UPDATE_PROGRESS = gql`
  mutation UpdateProgress($input: UpdateProgressInput!) {
    updateProgress(input: $input) { id currentPage }
  }
`;

export const FINISH_READING = gql`
  mutation FinishReading($input: FinishReadingInput!) {
    finishReading(input: $input) { id finishDate }
  }
`;