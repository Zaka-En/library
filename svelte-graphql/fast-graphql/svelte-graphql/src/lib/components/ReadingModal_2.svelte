<script lang="ts">
  import { graphql } from '$houdini';
  
  let { 
    isOpen = $bindable(false), 
    book, 
    reading 
  } = $props<{
    isOpen: boolean;
    book: BookType | null;
    reading: ReadingProgressType | null;
  }>();

  // --- Mutations ---
  const finishStore = graphql(`
    mutation FinishReading($input: FinishReadingInput!) {
      finishReading(input: $input) { id finishDate }
    }
  `);

  const updateStore = graphql(`
    mutation UpdateProgress($input: UpdateProgressInput!) {
      updateProgress(input: $input) { id currentPage }
    }
  `);

  
  let newPage = $state(0);
  let isSubmitting = $state(false);

  // Sincronizar la página del modal cuando se abre
  $effect(() => {
    if (isOpen && reading) {
      newPage = reading.currentPage;
    }
  });

  async function handleUpdate() {
    if (!reading) return;
    isSubmitting = true;
    await updateStore.mutate({ 
      input: { id: Number(reading.id), currentPage: newPage } 
    });
    isSubmitting = false;
    isOpen = false;
  }

  async function handleFinish() {
    if (!reading) return;
    isSubmitting = true;
    await finishStore.mutate({ 
      input: { id: Number(reading.id) } 
    });
    isSubmitting = false;
    isOpen = false;
  }
</script>

{#if isOpen && book && reading}
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-xl shadow-2xl max-w-sm w-full p-6 border border-gray-100">
      <h3 class="text-xl font-bold text-gray-800">{book.title}</h3>
      <p class="text-sm text-gray-500 mb-6">de {book.author?.name}</p>

      <div class="space-y-6">
        <div>
          <label for="pages" class="block text-sm font-medium text-gray-700 mb-2">
            ¿Por qué página vas? (Máx: {book.pages})
          </label>
          <div class="flex items-center gap-4">
            <input 
              type="number" 
              id="pages"
              bind:value={newPage}
              min="0"
              max={book.pages}
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            <button 
              onclick={handleUpdate}
              disabled={isSubmitting || (newPage === reading.currentPage)}
              class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50 transition-colors"
            >
              Actualizar
            </button>
          </div>
        </div>

        <hr class="border-gray-100" />

        <div class="flex flex-col gap-3">
          <p class="text-xs text-gray-400 text-center uppercase tracking-widest font-semibold">O también puedes</p>
          <button 
            onclick={handleFinish}
            disabled={isSubmitting}
            class="w-full py-3 px-4 border-2 border-green-500 text-green-600 font-bold rounded-lg hover:bg-green-50 transition-colors flex items-center justify-center gap-2"
          >
            🏁 ¡He terminado el libro!
          </button>
        </div>

        <button 
          onclick={() => isOpen = false}
          class="w-full text-gray-400 text-sm hover:text-gray-600 mt-2"
        >
          Cerrar ventana
        </button>
      </div>
    </div>
  </div>
{/if}