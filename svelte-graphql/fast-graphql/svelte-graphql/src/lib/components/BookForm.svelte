<script lang="ts">
  import type {LoaderType} from "$lib/utils/loader.svelte";
  import type { CreateBook$input
    , UpdateBook$input
    , QueryResult
    , UpdateBook$result
    , CreateBook$result
    , GetBooks$result 
    , GetAuthors$result,
    GetAuthorNamesWithId$result} from "$houdini";
  //import type {Timeout} from 'node:timers' <-- Typescript does not like it for some reason
  import FormButton from "./FormButton.svelte";
  import { goto } from "$app/navigation";
  import { graphql } from "$houdini";
  import { fade } from "svelte/transition";
  import { createLoader } from "$lib/utils/loader.svelte";

  interface Props{
    book:  GetBooks$result["books"][number] | null
    author : GetAuthors$result["authors"]["edges"][number]["node"] | null
    authorNames: GetAuthorNamesWithId$result["authorsQuery"] 
  }

  const { 
    book = null,
    author = null,
    authorNames = [],
   } : Props 
  = $props();


  let isEdit = $derived(!!book?.id);
  let error = $state("");
  let authorId: number | null = $state(null)
  let loader: LoaderType = createLoader()

  

  
  interface FormDataType {
    isbn?: string | null | undefined;
    pages?: number | null | undefined;
    publicationYear?: number | null | undefined;
    title?: string | null | undefined;
    authorId?: number | null | undefined;
  }

  let formData : FormDataType = $state({
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


  async function handleSubmit(e: Event) {

    e.preventDefault();

    //if(!validateInputs()) {return}

    loader.isLoading = true;
    error = "";


    let mutationResult: QueryResult<UpdateBook$result, UpdateBook$input>
                      | QueryResult<CreateBook$result, CreateBook$input> | null
                      = null
    try {
      
      if (isEdit && book?.id) {
        const input: UpdateBook$input = { 
        input: {
          id: Number(book.id),
          authorId: Number(author?.id), 
          title: formData.title,
          isbn: formData.isbn,
          pages: formData.pages,
          publicationYear: formData.publicationYear
        }};
        mutationResult = await updateBookStore.mutate(input);
      } else {
        const input: CreateBook$input = {
        input: {
          authorId: Number(author?.id) ,
          title: formData.title ?? "",  
          isbn: formData.isbn as string,
          pages: formData.pages as number,
          publicationYear: formData.publicationYear as number
          }
        };
        mutationResult = await createBookStore.mutate(input)
      }

    } catch (e) {
      error = "Algo ha pasado con el server"
    }

    loader.isLoading = false
    if (mutationResult?.errors) {     
      console.log(mutationResult.errors);
      error = mutationResult.errors[0].message
      if (error.includes("ISBN")) {
        error = `El isbn es un valor único universal, no puede ser duplicado`
      }
    } else {
      goto(`/books`)
    }


  }

  function handleCancel() {goto(`/books`)}



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
          minlength="3"
        />
      </div>

      <!-- ISBN -->
      <div >
        <label for="isbn" class="block text-sm font-medium text-gray-700 mb-2">
          ISBN
        </label>
       
        <div class="flex flex-col">
        
        
        <input
          name="isbn"
          id="isbn"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 isbn-input"
          placeholder="Ej: 1234567891234"
          pattern="[0-9]{13}"
        />
        <span class="isbn-error">
          Formato de ISBN inválido, debe ser exactamente 13 dígitos
        </span>
        
        
      </div>
        
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
            Escrito por {author?.fullname ? author.fullname : author?.name}
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
            {#each authorNames as author (author.id)}
              <option value={author.id}>{author.name}</option>
            {/each}
          </select>
        </div>
      {/if}

      <!-- Actions -->
      <div class="flex flex-col gap-3 pt-4">
        {#snippet submitSnippet(isLoading:any,editing:any)}
          {#if loader.isLoading}
            <span class="animate-spin mr-2">🛞</span> Cargando...
          {:else if editing !== undefined}
            <span>{editing ? 'Guardar' : 'Crear Nuevo'}</span>
          {/if}
        {/snippet}

        <FormButton loading={loader.isLoading} {isEdit} {submitSnippet}
          class="flex-1 bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        />

        <button
          type="button"
          onclick={handleCancel}
          disabled={loader.isLoading}
          class="flex-1 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          Cancelar
        </button>
        {#if loader.showSlowMessage}
          <p in:fade class="text-xs text-yellow-700 italic text-center">
            Está tardando un poco, tenga usted paciencia...
          </p>
        {/if}
      </div>
    </form>
  </div>
</section>


<style>
  
  .isbn-error {
    display: none;
    color: #dc2626;
    font-size: 14px;
    margin-top: 4px;
  }
  
  input.isbn-input:not(:focus):invalid:not(:placeholder-shown) + .isbn-error {
    display: block;
  }


</style>