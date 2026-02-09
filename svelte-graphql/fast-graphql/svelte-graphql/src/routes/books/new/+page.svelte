<script lang="ts">
  import BookForm from "$lib/components/BookForm.svelte";
  import type { PageProps } from "./$types";

  let { data } : PageProps = $props()
  let store =  $derived( data.authorNamesStore)
  let authorNames = $derived($store.data?.authorsQuery)
</script>

<BookForm {authorNames}  />