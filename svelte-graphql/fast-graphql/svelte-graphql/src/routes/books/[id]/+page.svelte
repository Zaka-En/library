<script lang="ts">
  import ReadingModal from "$lib/components/ReadingModal.svelte";
  
  const { data } = $props();
  const { book } = data;

  let isModalOpen = $state(false);

  function startReading() {
    isModalOpen = true;
  }
</script>

<section class="max-w-4xl mx-auto">
  <div class="bg-white rounded-lg shadow-lg overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-8">
      <h1 class="text-3xl font-bold mb-2">{book.title}</h1>
      {#if book.author}
        <p class="text-xl opacity-90">por {book.author.name}</p>
      {/if}
    </div>

    <!-- Book Info -->
    <div class="p-8">
      <div class="grid md:grid-cols-2 gap-8">
        <!-- Book Cover Placeholder -->
        <div class="flex justify-center">
          <div class="bg-gradient-to-br from-blue-400 to-purple-600 w-64 h-96 rounded-lg shadow-xl flex items-center justify-center">
            <span class="text-white text-8xl">📖</span>
          </div>
        </div>

        <!-- Book Details -->
        <div class="space-y-4">
          <div>
            <h2 class="text-2xl font-semibold mb-4">Detalles del Libro</h2>
          </div>

          <div class="space-y-3">
            <div>
              <span class="font-medium text-gray-700">Título:</span>
              <span class="ml-2">{book.title}</span>
            </div>

            <div>
              <span class="font-medium text-gray-700">ISBN:</span>
              <span class="ml-2">{book.isbn || 'No disponible'}</span>
            </div>

            <div>
              <span class="font-medium text-gray-700">Año de Publicación:</span>
              <span class="ml-2">{book.publicationYear}</span>
            </div>

            <div>
              <span class="font-medium text-gray-700">Páginas:</span>
              <span class="ml-2">{book.pages}</span>
            </div>

            {#if book.author}
              <div>
                <span class="font-medium text-gray-700">Autor:</span>
                <span class="ml-2">{book.author.name}</span>
                {#if book.author.country}
                  <span class="text-gray-500">({book.author.country})</span>
                {/if}
              </div>
            {/if}
          </div>

          <!-- Actions -->
          <div class="pt-6 space-y-3">
            <button 
              on:click={startReading}
              class="w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 transition font-medium"
            >
              📖 Empezar a Leer
            </button>

            <a 
              href="/books/{book.id}/edit"
              class="block w-full bg-yellow-600 text-white py-3 px-6 rounded-lg hover:bg-yellow-700 transition font-medium text-center"
            >
              ✏️ Editar Información
            </a>

            <a 
              href="/books"
              class="block w-full bg-gray-600 text-white py-3 px-6 rounded-lg hover:bg-gray-700 transition font-medium text-center"
            >
              ← Volver a Libros
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Reading Modal -->
<ReadingModal 
  bind:isOpen={isModalOpen} 
  book={book} 
  userId="user123"
/>