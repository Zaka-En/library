<script lang="ts">
  import { type Book } from '$lib/components/Book.svelte';
  import BookForm from '$lib/components/BookForm.svelte';
  import type { LayoutProps } from '../$types';

  const { data } : LayoutProps = $props();


  //Solución Temporal
  interface Author{
    readonly id: string;
    readonly name: string;
    readonly biography: string | null;
    readonly country: string;
    readonly fullname: string | null;
  }

  interface Book {
    readonly id: number;
    readonly title: string;
    readonly isbn: string;
    readonly publicationYear: number;
    readonly pages: number;
    readonly author: {
      readonly id: string;
      readonly name: string;
    } | null;
  }
  



  let bookStore = $derived(data.store)  
  let book = $derived($bookStore.data?.book ) as Book
  let author = $derived(book?.author) as Author

  


</script>

<BookForm {author} {book} authorNames={null}/>
