<script lang="ts">
  import Categories from "$lib/components/Categories.svelte";
  import { graphql } from "$houdini";
  import ReadingModal2 from "$lib/components/ReadingModal_2.svelte";
  import Reading from "$lib/components/Reading.svelte"
  import type { Snippet } from "svelte";

  
  const categories: CategoryType[] =  [
    {
      name: "Ciencia Ficción",
      description: "Viajes en el tiempo, distopías futuristas y exploración espacial.",
      totalBooks: 124
    },
    {
      name: "Filosofía",
      description: "Tratados clásicos y pensamientos contemporáneos sobre la existencia.",
      totalBooks: 86
    },
    {
      name: "Desarrollo Web",
      description: "Guías modernas sobre Svelte, Tailwind y arquitectura de software.",
      totalBooks: 52
    }
  ];

  const userId = 1

  const  myReadingProgressStore = graphql(
    `
      query MyReadingProgress($userId: Int!) {
        myReadingProgress(userId: $userId) {
          id currentPage startDate
          book {
            id title pages
            author { name }
          }
        }
      }
    `
  )


  $effect( () => {
    myReadingProgressStore.fetch({
      variables: {
        userId
      }
    })
  })

  const myReadingProgress = $derived($myReadingProgressStore.data?.myReadingProgress || [])


  let isModalOpen = $state(false);
  let selectedBook: BookType | null = $state(null);
  let selectedReading : ReadingProgressType | null = $state(null);

  function openReadingModal(book: BookType | null, reading: ReadingProgressType ) {
    selectedBook = book;
    selectedReading = reading;
    isModalOpen = true;
  }

</script>

{#if $myReadingProgressStore.fetching}
  <div class="animate-pulse">Cargando...</div>
{:else if $myReadingProgressStore.errors}
  <div class="bg-red-100 text-red-700 p-4 rounded">
    Ouups: ha habido un error al obtener sus datos. Contacta con el equipo de soporte
  </div>
{/if}




{#if myReadingProgress && !$myReadingProgressStore.fetching}
  <div>
    <h2 class="text-2xl font-bold mb-4 mt-2">📖 Leyendo Actualmente</h2>
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-9/12">
    
    {#each myReadingProgress as reading (reading.id)}
      {#if reading}
        <Reading 
          {reading} 
          onUpdate={() => openReadingModal(reading.book, reading)}
          />
      {/if}  
    {/each}
  </section>
  </div>
  
{/if}

{#snippet categorySnippet(name: string, description: string, totalBooks: number)} 
  <h5 class="font-bold text-gray-800 text-lg mb-1 capitalize mt-2">{name}</h5>
  <p class="text-sm text-gray-600 mb-4 leading-relaxed">
    {description?.length <= 50 ? description : description.slice(0, 50)}...
  </p>
  <a href="/books" class="px-3 py-1 bg-indigo-600 text-white text-xs font-semibold rounded-full hover:bg-indigo-700 transition-colors">
    <span class="mr-1">{totalBooks}</span> libros
  </a>
{/snippet}

<Categories {categories} {categorySnippet} >

  {#snippet children(cat: CategoryType,renderSnippet: Snippet<[string,string,number]>)}
    {@render renderSnippet(cat.name,cat.description,cat.totalBooks)}
  {/snippet}

</Categories>

<!-- Reading Modal -->
<ReadingModal2
  bind:isOpen={isModalOpen} 
  book={selectedBook} 
  reading={selectedReading}
/>

