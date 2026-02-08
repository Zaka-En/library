<script lang="ts">
  import AuthorsList from "$lib/components/AuthorsList.svelte";
  import { graphql } from "$houdini"; 
  import PaginationNav from "$lib/components/PaginationNav.svelte";

  const authorsStore = graphql(
    `
      query GetAuthors($first: Int, $last: Int  $after: String, $before: String) {
        authors(first: $first, last: $last, after: $after, before: $before) 
        @list(name: "All_Authors") 
        @paginate(mode: SinglePage) {  
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
          totalCount
        }
        }
      }
    `
  );

  // Forzamos el fetch inicial 
  $effect(() => {
    authorsStore.fetch({variables:{first: 10}});
  });

  
  let authors = $derived.by(() => {
    return $authorsStore.data?.authors?.edges.map(edge => edge.node) ?? []
  });

  let pageInfo = $derived($authorsStore.pageInfo)
  let fetching = $derived($authorsStore.fetching)
  

  
</script>

<section class="w-full">
  <div class="flex justify-between items-center mb-7">
    
      <h1 class="text-3xl font-bold">Autores</h1>
      
      <PaginationNav
        {pageInfo}
        fetching={fetching}
        itemsPorPage={10}
        onNext={(cursor) => authorsStore.loadNextPage({
          first: 10,
          after: cursor,
        })}
        onPrevious={(cursor) => authorsStore.loadPreviousPage({
          last: 10,
          before: cursor,
        })}
      />

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