<script lang="ts">
  import { UPDATE_BOOK } from "$lib/graphql/mutations";
  import { client as mutationClient } from "$lib/graphql/client";
  import { goto } from "$app/navigation";

  const { data } = $props();
  const { book, authors } = data;

  let title = $state(book.title);
  let isbn = $state(book.isbn || '');
  let publicationYear = $state(book.publicationYear);
  let pages = $state(book.pages);
  let authorId = $state(book.author?.id || '');
  let isLoading = $state(false);
  let error = $state('');

  async function handleSubmit(event: Event) {
    event.preventDefault();
    isLoading = true;
    error = '';

    try {
      const result = await mutationClient.mutation(UPDATE_BOOK, {
        input: {
          id: book.id,
          title,
          isbn,
          publicationYear: parseInt(publicationYear),
          pages: parseInt(pages),
          authorId: parseInt(authorId)
        }
      }).toPromise();

      if (result.error) {
        error = result.error.message;
      } else {
        await goto(`/books/${book.id}`);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Error al actualizar el libro';
    } finally {
      isLoading = false;
    }
  }

  function handleCancel() {
    goto(`/books/${book.id}`);
  }
</script>

<section class="max-w-2xl mx-auto">
  <div class="bg-white rounded-lg shadow-lg overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-yellow-500 to-orange-600 text-white p-6">
      <h1 class="text-2xl font-bold">Editar Libro</h1>
      <p class="opacity-90 mt-1">Modifica la información del libro</p>
    </div>

    <!-- Form -->
    <form on:submit={handleSubmit} class="p-6 space-y-6">
      {#if error}
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      {/if}

      <!-- Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
          Título del Libro
        </label>
        <input
          id="title"
          type="text"
          bind:value={title}
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Ingrese el título del libro"
        />
      </div>

      <!-- ISBN -->
      <div>
        <label for="isbn" class="block text-sm font-medium text-gray-700 mb-2">
          ISBN
        </label>
        <input
          id="isbn"
          type="text"
          bind:value={isbn}
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Ingrese el ISBN (opcional)"
        />
      </div>

      <!-- Publication Year and Pages -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="publicationYear" class="block text-sm font-medium text-gray-700 mb-2">
            Año de Publicación
          </label>
          <input
            id="publicationYear"
            type="number"
            bind:value={publicationYear}
            required
            min="1000"
            max={new Date().getFullYear()}
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label for="pages" class="block text-sm font-medium text-gray-700 mb-2">
            Número de Páginas
          </label>
          <input
            id="pages"
            type="number"
            bind:value={pages}
            required
            min="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      <!-- Author -->
      <div>
        <label for="authorId" class="block text-sm font-medium text-gray-700 mb-2">
          Autor
        </label>
        <select
          id="authorId"
          bind:value={authorId}
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Seleccione un autor</option>
          {#each authors as author}
            <option value={author.id}>{author.name}</option>
          {/each}
        </select>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={isLoading}
          class="flex-1 bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {#if isLoading}
            Guardando...
          {:else}
            💾 Guardar Cambios
          {/if}
        </button>

        <button
          type="button"
          on:click={handleCancel}
          disabled={isLoading}
          class="flex-1 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          ❌ Cancelar
        </button>
      </div>
    </form>
  </div>
</section>