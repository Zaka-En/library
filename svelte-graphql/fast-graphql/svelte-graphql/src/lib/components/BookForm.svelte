<script lang="ts">



  import { goto } from "$app/navigation";
  import { graphql } from "$houdini";
  const { book = null, author = null, event = null } = $props();
  let isEdit = $derived(!!book?.id);
  let error = $state("");
  let isLoading = $state(false);
  let authorId: number | null = $state(null)

  let formData = $state({
    title: "",
    isbn: null,
    publicationYear: null,
    pages: null,
  });

  $effect(() => {
    formData.title = book?.title;
    formData.isbn = book?.isbn;
    formData.publicationYear = book?.publicationYear;
    formData.pages = book?.pages;
  });

  

  const authorNamesStore = graphql(`
    query GetAuthorNamesWithId{
      authors{
        id
        name
      }
    }
  `)

  const updateBookStore = graphql(`
    mutation UpdateBook($input: UpdateBookInput!) {
      updateBook(input: $input) { 
        id title isbn publicationYear pages 
        author { id name country }
      }
    }
  `)

  const createBookStore = graphql(`
    mutation CreateBook($input: CreateBookInput!) {
      createBook(input: $input) { id title }
    }
  `)


  // the author name loaded in case of creating new Book
  if (!isEdit && event) {
    authorNamesStore.fetch({event}); 
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    isLoading = true;
    error = "";

    let mutationResult; //<-- el resultado de las mutacions

    let variables = isEdit
      ? { input: {id: Number(book.id), authorId: author.id, ...formData} }
      : { input: { authorId, ...formData } };

    if (isEdit) {
      mutationResult = await updateBookStore.mutate(variables);
    }else if(!isEdit && authorId) {
      console.log(variables)
      mutationResult = await createBookStore.mutate(variables);      
    }

    isLoading = false
    if (mutationResult.errors) {     
      error = isEdit? "Ha ocurrido un error al intentar modificar los datos . Vuleve a enviar el formulario." : "Ha ocurrido un error al intentar insertar los datos vuleve a enviar el formulario."
      console.log(mutationResult?.errors);
      
    } else {
      goto(`/books/${book.id}`)
    }


  }

  function handleCancel() {goto(`/books`)}

  async function loadAuthorNames() {
    await authorNamesStore.fetch();
  }

</script>

<section class="max-w-2xl mx-auto">
  <div class="bg-white rounded-lg shadow-lg overflow-hidden">
    <!-- Header -->
    <div class="bg-linear-to-r from-yellow-500 to-orange-600 text-white p-6">
      <h1 class="text-2xl font-bold">
        {isEdit ? "Editar Libro" : "Crear nuevo Libro"}
      </h1>
      <p class="opacity-90 mt-1">Modifica/Inserta la información del libro</p>
    </div>

    <!-- Form -->
    <form onsubmit={handleSubmit} class="p-6 space-y-6">
      {#if error}
        <div
          class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"
        >
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
          bind:value={formData.title}
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
          bind:value={formData.isbn}
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Ingrese el ISBN (opcional)"
        />
      </div>

      <!-- Publication Year and Pages -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label
            for="publicationYear"
            class="block text-sm font-medium text-gray-700 mb-2"
          >
            Año de Publicación
          </label>
          <input
            id="publicationYear"
            type="number"
            bind:value={formData.publicationYear}
            required
            min="1000"
            max={new Date().getFullYear()}
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label
            for="pages"
            class="block text-sm font-medium text-gray-700 mb-2"
          >
            Número de Páginas
          </label>
          <input
            id="pages"
            type="number"
            bind:value={formData.pages}
            required
            min="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      <!-- Author  -->
      {#if isEdit}
        <div>
          <p class="block text-sm font-medium text-gray-700 mb-2">
            Escrito por {author?.fullname ? author.fullname : author.name}
          </p>
        </div>
      {:else }
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
            {#each $authorNamesStore.data?.authors as author (author.id)}
              <option value={author.id}>{author.name}</option>
            {/each}
          </select>
        </div>
      {/if}

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
            Guardar
          {/if}
        </button>

        <button
          type="button"
          onclick={handleCancel}
          disabled={isLoading}
          class="flex-1 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          Cancelar
        </button>
      </div>
    </form>
  </div>
</section>
