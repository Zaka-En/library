<script lang="ts">
  import FormButton from "./FormButton.svelte";
  import { goto } from "$app/navigation";
  import { graphql } from "$houdini";
  import { fade } from "svelte/transition";
  const { book = null, author = null, event = null } = $props();
  let isEdit = $derived(!!book?.id);
  let error = $state("");
  let isLoading = $state(false);
  let authorId: number | null = $state(null)
  let showSlowMessage = $state(false)


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

  $effect(() => {
    let timerId = null
    if (isLoading) {
      timerId = setTimeout(()=>{
        showSlowMessage = true
      },1000)
    }

    return () => {
      clearTimeout(timerId)
      showSlowMessage  = false        

    }
  })

  $inspect(showSlowMessage)

  

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

    if(!validateInputs()) {return}

    isLoading = true;
    error = "";

    let mutationResult; //<-- el resultado de las mutacions

    let variables = isEdit
      ? { input: {id: Number(book.id), authorId: author.id, ...formData} }
      : { input: { authorId, ...formData } };

    try {
      if (isEdit) {
        mutationResult = await updateBookStore.mutate(variables);
      }else if(!isEdit && authorId) {
        mutationResult = await createBookStore.mutate(variables);      
      }
    } catch (e) {
      error = "Algo ha pasado con el server"
    }

    isLoading = false
    if (mutationResult?.errors) {     
      console.log(mutationResult.errors);
      error = mutationResult.errors[0].message
      // if (error.includes("ISBN")) {
      //   error = `El isbn es un valor único universal, no puede ser duplicado`
      // }
    } else {
      goto(`/books`)
    }


  }

  function handleCancel() {goto(`/books`)}

  function validateInputs(): boolean {
    if (!formData.title || formData.title.trim().length < 2) {
      error = "El título es obligatorio y debe tener al menos 2 caracteres.";
      return false;
    }

    if (!authorId) {
      error = "Debes seleccionar un autor para el libro.";
      return false;
    }

    // Validación de ISBN (ejemplo simple de longitud)
    if (formData.isbn && formData.isbn.length < 13) {
      error = "El ISBN debe tener al menos 13 dígitos.";
      return false;
    }

    if (formData.publicationYear && (formData.publicationYear < 1000 || formData.publicationYear > 2026)) {
      error = "El año de publicación no es válido.";
      return false;
    }

    return true;
  }

  async function loadAuthorNames() {
    await authorNamesStore.fetch();
  }

</script>

<section class="max-w-xl mx-auto">
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
      <div class="flex flex-col gap-3 pt-4">
        {#snippet submitSnippet(isLoading:any,editing:any)}
          {#if isLoading}
            <span class="animate-spin mr-2">🛞</span> Cargando...
          {:else if editing !== undefined}
            <span>{editing ? 'Guardar' : 'Crear Nuevo'}</span>
          {/if}
        {/snippet}

        <FormButton loading={isLoading} {isEdit} {submitSnippet}
          class="flex-1 bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        />

        <button
          type="button"
          onclick={handleCancel}
          disabled={isLoading}
          class="flex-1 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          Cancelar
        </button>
        {#if showSlowMessage}
          <p in:fade class="text-xs text-yellow-700 italic text-center">
            Está tardando un poco, tenga usted paciencia...
          </p>
        {/if}
      </div>
    </form>
  </div>
</section>
