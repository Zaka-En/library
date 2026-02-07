<script lang="ts">
  import AuthorsList from "$lib/components/AuthorsList.svelte";
  import { graphql } from "$houdini"; 

  const authorsStore = graphql(
    `
      query GetAuthors($first: Int, $last: Int  $after: String, $before: String) {
        authors(first: $first, last: $last, after: $after, before: $before) @list(name: "All_Authors") @paginate(mode: SinglePage) { 
          
          edges {
          node {
            id
            name
            fullname
            biography
            country
          }
          }
        pageInfo {
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }
        }
      }
    `
  );

  // Forzamos el fetch inicial si es necesario
  $effect(() => {
    authorsStore.fetch({variables:{first: 10}});
  });

  // Derivamos los datos de forma segura para Svelte 5
  let authors = $derived.by(() => {
    return $authorsStore.data?.authors?.edges.map(edge => edge.node) ?? []
  });

  $inspect($authorsStore?.pageInfo)
</script>

<section class="w-full">
  <div class="flex justify-between items-center mb-7">
    
      <h1 class="text-3xl font-bold">Autores</h1>
      
      <div class="flex  items-center gap-2 bg-gray-100 p-1 rounded-full border">
        <button
          onclick={() => authorsStore.loadPreviousPage({last: 10, before: $authorsStore.data?.authors?.pageInfo?.startCursor ?? undefined})}
         
          disabled={!$authorsStore.pageInfo?.hasPreviousPage || $authorsStore.fetching}
          class="w-8 h-8 flex items-center justify-center rounded-full bg-white shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          aria-label="Página anterior"
        >
          <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <span class="text-xs font-medium text-gray-500 px-1">
          {#if $authorsStore.fetching}
             ...
          {:else}
             Pág
          {/if}
        </span>

        <button
          onclick={() => authorsStore.loadNextPage({first: 10 , after: $authorsStore.data?.authors?.pageInfo?.endCursor ?? undefined})}
          disabled={!$authorsStore.pageInfo?.hasNextPage || $authorsStore.fetching}
          class="w-8 h-8 flex items-center justify-center rounded-full bg-white shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          aria-label="Siguiente página"
        >
          <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      <a
        href="/authors/new"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors shadow-sm"
      >
        + Nuevo Autor
      </a>
    
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2">
    <AuthorsList {authors} />
  </div>
</section>