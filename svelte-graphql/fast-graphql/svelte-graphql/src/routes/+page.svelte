<script lang="ts">

  import { graphql } from "$houdini";
  import ReadingModal from "$lib/components/ReadingModal.svelte";
  import Reading from "$lib/components/Reading.svelte";

  const userId = 'user123'

  let myReadingProgressStore = graphql(
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
  let selectedBook = $state(null);
  let selectedReading = $state(null);

  function openReadingModal(book: any, reading: any = null) {
    selectedBook = book;
    selectedReading = reading;
    isModalOpen = true;
  }

  function closeModal() {
    isModalOpen = false;
    selectedBook = null;
    selectedReading = null;
  }
</script>

{#if $myReadingProgressStore.fetching}
  <div class="animate-pulse">Cargando...</div>
{:else if $myReadingProgressStore.errors}
  <div class="bg-red-100 text-red-700 p-4 rounded">
    Ouups: ha habido un error al obtener sus datos. Contacta con el equipo de soporte
  </div>
{/if}




{#if myReadingProgress}
  <h2 class="text-2xl font-bold mb-4">📖 Leyendo Actualmente</h2>
  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each myReadingProgress as reading (reading.id)}
      <Reading 
        {reading} 
        onUpdate={(book, readingData) => openReadingModal(book, readingData)}
        onFinish={(book, readingData) => openReadingModal(book, readingData)}
      />
    {/each}
  </section>
{/if}

<!-- Reading Modal -->
<ReadingModal 
  bind:isOpen={isModalOpen} 
  book={selectedBook} 
  userId="user123"
/>



