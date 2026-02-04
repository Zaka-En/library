<script lang="ts">
  import AuthorForm from "$lib/components/AuthorForm.svelte";
  import type { LayoutProps } from "./$types";

  let { data } : LayoutProps = $props()
  
  let authorStore = $derived(data.store)
  let author = $derived($authorStore.data?.author)


</script>

<AuthorForm author={author}/>