<script lang="ts">

  import type { LayoutProps } from "./$types";


  let {data} : LayoutProps = $props()

  let authorStore = $derived(data.store)
  let author = $derived($authorStore.data?.author)
  let fetching = $derived($authorStore.fetching)

</script>

{#if !$authorStore.fetching && author}
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
    <h1 class="text-3xl font-semibold mb-2">
      {author.name}
    </h1>
    

    <p class="text-gray-500 mb-6">
      {author?.fullname} · {author.country}
    </p>

    {#if author?.biography}
      <p class="text-gray-700 leading-relaxed mb-8">
        {author?.biography}
      </p>
    {/if}

    <div>
      <h2 class="text-xl font-medium mb-4">Libros</h2>

      {#if author?.books?.length}
        <ul class="space-y-3">
          {#each author.books as book}
            <li>
              <a
                href={`/book/${book.id}`}
                class="block p-4 rounded-lg border border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition"
              >
                <div class="flex justify-between items-center">
                  <span class="font-medium text-gray-800">
                    {book.title}
                  </span>
                  <span class="text-sm text-gray-500">
                    {book.publicationYear}
                  </span>
                </div>

                <p class="text-sm text-gray-500 mt-1">
                  {book.pages} páginas
                </p>
              </a>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="text-gray-400">Este autor no tiene libros registrados.</p>
      {/if}
    </div>
  </div>
{/if}