<script lang="ts">
  import AuthorsList from "$lib/components/AuthorsList.svelte";
  import { graphql } from "$houdini"; 
  import type { PageProps } from "./$types";

  let { data } : PageProps = $props()
  let { user } = $derived(data)


  const authorsStore =  $derived(data.GetAuthors)
  
  let authors = $derived($authorsStore.data?.authors?.edges ?? []);
  let pageInfo = $derived($authorsStore.data?.authors.pageInfo)
  let fetching = $derived($authorsStore.fetching)
  
  
</script>

<section class="w-full mx-10">
  <div class="flex justify-between items-center mb-7">
    
      <h1 class="text-3xl font-bold">Autores</h1>
      {#if user?.rol === "admin"}
        <a
          href="/authors/new"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors shadow-sm"
        >
          + Nuevo Autor
        </a>
      {/if}
    
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2">
    <AuthorsList 
  
    noMoreData = {!pageInfo.hasNextPage}
    loading = {fetching}
    onLoadMore= {() => {
      authorsStore.loadNextPage({
        first: 10
      })
    }}
    {authors}
    />
  </div>
</section>