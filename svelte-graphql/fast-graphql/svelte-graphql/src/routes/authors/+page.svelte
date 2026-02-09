<script lang="ts">
  import AuthorsList from "$lib/components/AuthorsList.svelte";
  import { graphql } from "$houdini"; 
  import PaginationNav from "$lib/components/PaginationNav.svelte";


  const authorsStore = graphql(
    `
      query GetAuthors($first: Int, $after: String) {
        authors(first: $first, after: $after)
        @paginate(mode: Infinite)
        @list(name: "All_Authors") {  
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

  // $effect(() => {
  //   const freshData = $authorsStore.data?.authors.edges.map(edge => edge.node) ?? []

  //   if (freshData?.length > 0) {
  //     const combined = [ ...authors, ...freshData]
  //     const uniqueAuthors = Array.from(new Map(combined.map(a => [a.id, a])).values())
  //     authors = uniqueAuthors
  //   }
  // })
  
  let authors = $derived($authorsStore.data?.authors?.edges.map(e => e.node) ?? []);
  let pageInfo = $derived($authorsStore.pageInfo)
  let fetching = $derived($authorsStore.fetching)
  
  $inspect(authors)
  
</script>

<section class="w-full">
  <div class="flex justify-between items-center mb-7">
    
      <h1 class="text-3xl font-bold">Autores</h1>
      
      <!-- <PaginationNav
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
      /> -->

      <a
        href="/authors/new"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors shadow-sm"
      >
        + Nuevo Autor
      </a>
    
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2">
    <AuthorsList 
  
    noMoreData = {!pageInfo.hasNextPage}
    loading = {$authorsStore.fetching}
    onLoadMore= {() => {
      authorsStore.loadNextPage({
        first: 10
      })
    }}
    {authors}
    />
  </div>
</section>