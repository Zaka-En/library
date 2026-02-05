<script lang="ts">
  import BookForm from '$lib/components/BookForm.svelte';
  import type { LayoutProps } from './$types';

  const { data } : LayoutProps = $props();

  let bookStore = $derived(data.store)  
  let book = $derived($bookStore.data?.book )
  let author = $derived(book?.author)


</script>

<BookForm {author} {book} />
