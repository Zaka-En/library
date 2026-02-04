<script lang="ts">

  import { graphql } from "$houdini";
  import ReadingModal2 from "$lib/components/ReadingModal_2.svelte";
  import Reading from "$lib/components/Reading.svelte"

  const userId = '1'

  const  myReadingProgressStore = graphql(
    `
      query MyReadingProgress($userId: String!) {
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
  <h2 class="text-2xl font-bold mb-4">📖 Leyendo Actualmente</h2>
  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each myReadingProgress as reading (reading.id)}
      {#if reading}
        <Reading 
          {reading} 
          onUpdate={() => openReadingModal(reading.book, reading)}
           
        />
      {/if}  
    {/each}
  </section>
{/if}

<!-- Reading Modal -->
<ReadingModal2
  bind:isOpen={isModalOpen} 
  book={selectedBook} 
  reading={selectedReading}
/>



