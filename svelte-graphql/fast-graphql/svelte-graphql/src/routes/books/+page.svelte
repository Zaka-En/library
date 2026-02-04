<script lang="ts">
  import Book from '$lib/components/Book.svelte';
  import type { PageProps } from './$types';

  const { data } = $props()

  let booksStore = $derived(data.store)
  
  let books = $derived($booksStore.data?.books)

</script>

<section>
  <div class="flex justify-between items-center mb-7">
    <h1 class="text-3xl font-bold">Libros</h1>
   
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
    {#each books as book (book.id)}
      <Book {book} />
    {/each}
  </div>
</section>