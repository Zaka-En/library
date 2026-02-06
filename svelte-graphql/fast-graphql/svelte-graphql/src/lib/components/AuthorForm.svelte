<script lang="ts">
  import { graphql } from "$houdini";
  import { goto } from "$app/navigation";
  import FormButton from "./FormButton.svelte";
  let { author = null } = $props();


  let isEdit = $derived(!!author?.id);
  let loading = $state(false);
  let errorMessage = $state("");
  

  interface formDataType{
    name:  string
    fullname: string
    biography: string
    country: string
  }

  // Estado del formulario usando el rune $state
  let formData : formDataType  = $state({
    name:  "",
    fullname:  "",
    biography: "",
    country: "",
  });


  // when the componente is mounted, it retries the author data if not null
  $effect(() => {
    formData.name = author?.name ?? "";
    formData.fullname = author?.fullname ?? "";
    formData.biography = author?.biography ?? "";
    formData.country = author?.country ?? "";
  })

  const createAuthorStore = graphql(`
      mutation CreateAuthor($input: CreateAuthorInput!) {
      createAuthor(input: $input) 
      { id @optimisticKey        
        name 
        fullname 
        biography 
        country
      ...All_Authors_insert  
      }
    }
  `)

  const updateAuthorStore = graphql(`
      mutation UpdateAuthor($input: UpdateAuthorInput!) {
        updateAuthor(input: $input) { id name biography country }
      }
  `)

  

  async function handleSubmit(e: Event) {

    //Handling empty inputs
    if (formData.name.trim() === "") {
      errorMessage = "El campo <strong>Nombre</strong> no puede ser vacío"
      return
    }else if(formData.country.trim() === ""){
      errorMessage = "El campo <strong>País</strong> no puede ser vacío"
      return
    }


    e.preventDefault();
    loading = true;
    errorMessage = "";

    let result


    interface inputType{
      name: string
      fullname?: string | null
      biography?: string | null
      country: string
    }
      goto("/authors");


    
    const input: inputType = {
      name: formData.name,
      fullname: formData.fullname || null,
      biography: formData.biography || null,
      country: formData.country
    };
    
    
    const variables = isEdit 
    ? { input: { id: Number(author.id), ...input } } 
    : { input };

    if (isEdit) {
      result = await updateAuthorStore.mutate(variables)
    }else{
      result = await createAuthorStore
      .mutate(
        variables,
        {
          optimisticResponse:{
            createAuthor: {
              name: formData.name,
              fullname: formData.fullname,
              biography: formData.biography,
              country: formData.country,
            }
          }
        }
      )
    }

    

    loading = false;

    if (result.errors) {
      errorMessage = "Ocurrió un error al subir los datos"
    } else {
      
      goto("/authors");
    }
  }
</script>

<form onsubmit={handleSubmit} class="space-y-4 max-w-lg mx-auto bg-white p-8 rounded-xl shadow-md">
  <h2 class="text-2xl font-bold mb-6">
    {isEdit ? 'Editar Autor' : 'Nuevo Autor'}
  </h2>

  {#if errorMessage}
    <div class="p-3 bg-red-100 text-red-700 rounded-lg text-sm">
      {errorMessage}
    </div>
  {/if}

  {#if isEdit}
    <div>
      <label class="block text-sm font-medium text-gray-700" for="id">ID del Autor</label>
      <input
        id="id"
        type="text"
        value={author.id}
        disabled
        class="mt-1 block w-full rounded-md border-gray-30 bg-gray-100 cursor-not-allowed"
      />
    </div>
  {/if}

  <div>
    <label class="block text-sm font-medium text-gray-700" for="name">Nombre (obligatorio)</label>
    <input
      id="name"
      bind:value={formData.name}
      type="text"
      required
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    />
  </div>

  <div>
    <label class="block text-sm font-medium text-gray-700" for="fullname">Nombre Completo</label>
    <input
      id="fullname"
      bind:value={formData.fullname}
      type="text"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    />
  </div>

  <div>
    <label class="block text-sm font-medium text-gray-700" for="country">País (obligatorio)</label>
    <input
      id="country"
      bind:value={formData.country}
      type="text"
      required
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    />
  </div>


  <div>
    <label class="block text-sm font-medium text-gray-700" for="biography">Biografía</label>
    <textarea
      id="biography"
      bind:value={formData.biography}
      rows="4"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    ></textarea>
  </div>

  
  
  {#snippet submitSnippet(isLoading:any,editing:any)}
    {#if isLoading}
      <span class="animate-spin mr-2">🛞</span> Cargando...
    {:else if editing !== undefined}
      <span>{editing ? 'Guardar Cambios' : 'Crear Nuevo'}</span>
    {/if}
  {/snippet}

  <div class="pt-4">
    <FormButton  {loading} {isEdit} {submitSnippet} 
    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300"
    />
  </div>

  
</form>