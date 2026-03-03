<script lang="ts">
  import BookForm from "$lib/components/BookForm.svelte";
  import type { PageProps } from "./$types";

  interface AuthorNameId{
    readonly id: string;
    readonly name: string;
  }

  let { data } : PageProps = $props()
  let store =  $derived( data.authorNamesStore)
  let authorNames = $derived($store.data?.authorsQuery ?? []) as AuthorNameId[]
</script>

<BookForm {authorNames} book = {null} author={null} />