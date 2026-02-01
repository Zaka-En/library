<script lang="ts">
  import { START_READING, UPDATE_PROGRESS, FINISH_READING } from "$lib/graphql/mutations";
  import { client } from "$lib/graphql/client";
  import { MY_READING_PROGRESS } from "$lib/graphql/queries";

  interface Book {
    id: number;
    title: string;
    pages: number;
  }

  interface ReadingProgress {
    id: number;
    currentPage: number;
    startDate: string;
    finishDate?: string;
    book: Book;
  }

  let { isOpen = $bindable(false), book = null, userId = '' } = $props<{
    isOpen: boolean;
    book: Book | null;
    userId: string;
  }>();

  let action = $state<'start' | 'update' | 'finish'>('start');
  let currentPage = $state(1);
  let isLoading = $state(false);
  let error = $state('');
  let success = $state('');

  let readingProgress = $state<ReadingProgress | null>(null);

  $effect(() => {
    if (isOpen && book && userId) {
      loadReadingProgress();
    }
  });

  async function loadReadingProgress() {
    try {
      const result = await client.query(MY_READING_PROGRESS, { userId }).toPromise();
      if (result.data?.myReadingProgress) {
        const progress = result.data.myReadingProgress.find((p: ReadingProgress) => p.book.id === book?.id);
        if (progress) {
          readingProgress = progress;
          currentPage = progress.currentPage;
          action = 'update';
        } else {
          readingProgress = null;
          action = 'start';
        }
      }
    } catch (err) {
      console.error('Error loading reading progress:', err);
    }
  }

  async function handleSubmit() {
    if (!book || !userId) return;

    isLoading = true;
    error = '';
    success = '';

    try {
      let result;

      switch (action) {
        case 'start':
          result = await client.mutation(START_READING, {
            input: {
              bookId: book.id,
              userId            }
          }).toPromise();
          success = '¡Lectura iniciada exitosamente!';
          break;

        case 'update':
          result = await client.mutation(UPDATE_PROGRESS, {
            input: {
              id: readingProgress?.id,
              currentPage
            }
          }).toPromise();
          success = '¡Progreso actualizado exitosamente!';
          break;

        case 'finish':
          result = await client.mutation(FINISH_READING, {
            input: {
              id: readingProgress?.id
            }
          }).toPromise();
          success = '¡Felicidades! Libro completado.';
          break;
      }

      if (result.error) {
        error = result.error.message;
      } else {
        setTimeout(() => {
          isOpen = false;
          success = '';
          error = '';
        }, 500);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Error al procesar la acción';
    } finally {
      isLoading = false;
    }
  }

  function closeModal() {
    isOpen = false;
    success = '';
    error = '';
  }

  function getActionText() {
    switch (action) {
      case 'start': return 'Iniciar Lectura';
      case 'update': return 'Actualizar Progreso';
      case 'finish': return 'Finalizar Lectura';
      default: return '';
    }
  }

  function getActionButtonColor() {
    switch (action) {
      case 'start': return 'bg-green-600 hover:bg-green-700';
      case 'update': return 'bg-blue-600 hover:bg-blue-700';
      case 'finish': return 'bg-purple-600 hover:bg-purple-700';
      default: return '';
    }
  }
</script>

{#if isOpen}
  <div class="fixed inset-0 bg-black/30 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="bg-linear-to-r from-indigo-500 to-purple-600 text-white p-6 rounded-t-lg">
        <h2 class="text-xl font-bold">
          {book?.title}
        </h2>
        <p class="text-sm opacity-90 mt-1">Gestionar estado de lectura</p>
      </div>

      <!-- Content -->
      <div class="p-6">
        {#if error}
          <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        {/if}

        {#if success}
          <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {success}
          </div>
        {/if}

        <!-- Current Reading Status -->
        {#if readingProgress}
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <h3 class="font-semibold text-blue-800 mb-2">Estado Actual</h3>
            <p class="text-sm text-blue-700">
              Página actual: <span class="font-medium">{readingProgress.currentPage}</span> de <span class="font-medium">{book?.pages}</span>
            </p>
            <p class="text-sm text-blue-700">
              Iniciado: {new Date(readingProgress.startDate).toLocaleDateString('es-ES')}
            </p>
            {#if readingProgress.finishDate}
              <p class="text-sm text-green-700 font-medium">
                Finalizado: {new Date(readingProgress.finishDate).toLocaleDateString('es-ES')}
              </p>
            {/if}
          </div>
        {/if}

        <!-- Action Selection -->
        <div class="mb-4">
          <p class="block text-sm font-medium text-gray-700 mb-2">
            Acción
          </p>
          <div class="space-y-2">
            {#if !readingProgress}
              <label class="flex items-center">
                <input
                  type="radio"
                  bind:group={action}
                  value="start"
                  class="mr-2"
                />
                <span class="text-sm">Iniciar lectura</span>
              </label>
            {/if}

            {#if readingProgress && !readingProgress.finishDate}
              <label class="flex items-center">
                <input
                  type="radio"
                  bind:group={action}
                  value="update"
                  class="mr-2"
                />
                <span class="text-sm">Actualizar progreso</span>
              </label>

              <label class="flex items-center">
                <input
                  type="radio"
                  bind:group={action}
                  value="finish"
                  class="mr-2"
                />
                <span class="text-sm">Finalizar lectura</span>
              </label>
            {/if}
          </div>
        </div>

        <!-- Current Page Input -->
        {#if action === 'update' && book}
          <div class="mb-4">
            <label for="currentPage" class="block text-sm font-medium text-gray-700 mb-2">
              Página Actual
            </label>
            <input
              id="currentPage"
              type="number"
              bind:value={currentPage}
              min="1"
              max={book.pages}
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
            <p class="text-xs text-gray-500 mt-1">
              Página {currentPage} de {book.pages} ({Math.round((currentPage / book.pages) * 100)}% completado)
            </p>
          </div>
        {/if}

        <!-- Action Buttons -->
        <div class="flex gap-3">
          <button
            onclick={handleSubmit}
            disabled={isLoading}
              class="flex-1 {getActionButtonColor()} text-white py-2 px-4 rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {#if isLoading}
              Procesando...
            {:else}
              {getActionText()}
            {/if}
          </button>

          <button
            onclick={closeModal}
            disabled={isLoading}
            class="flex-1 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}