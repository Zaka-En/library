<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import { getContextClient } from "@urql/svelte";
  import { MY_READING_PROGRESS } from "$lib/graphql/queries";
  import Reading from "$lib/components/Reading.svelte";
  import ReadingModal from "$lib/components/ReadingModal.svelte";

  const userId = 'user123'
  const resultMyReadingProgress = queryStore({
    client: getContextClient(),
    query: MY_READING_PROGRESS,
    variables: {userId}
  });

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

{#if $resultMyReadingProgress.fetching}
  <div class="animate-pulse">Cargando...</div>
{:else if $resultMyReadingProgress.error}
  <div class="bg-red-100 text-red-700 p-4 rounded">
    Ouups: ha habido un error al obtener sus datos. Contacta con el equipo de soporte
  </div>
{/if}




{#if $resultMyReadingProgress?.data?.myReadingProgress}
  <h2 class="text-2xl font-bold mb-4">📖 Leyendo Actualmente</h2>
  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each $resultMyReadingProgress.data.myReadingProgress as reading (reading.id)}
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



