<script lang="ts">
  import { graphql } from '$houdini';
  import type { LayoutProps } from './$types';
 import { goto } from '$app/navigation';

  const { data } : LayoutProps = $props();

  let bookStore = $derived(data.store)  
  let book = $derived($bookStore.data?.book )
  let isFetching = $derived($bookStore.fetching)
  let author = $derived(book?.author)

  let birthDay: Date|null = $state(null)
	let birthDayInput: string = $state("")

	let birthDayObject= {
		get birthDay(): Date | null{
			return birthDay;
		} ,
		get birthDayInput(): string{
			return birthDayInput;
		},
		
		set birthDay(val: Date){
			birthDay = val
			let isostr = val.toISOString().split("T")[0]
			birthDayInput = isostr
		},
		
		set birthDayInput(val: string){
			birthDayInput = val
			birthDay = new Date(val)
		}
	}

  const startReadingStore = graphql(
    `
      mutation StartReading($input: StartReadingInput!){
        startReading(input: $input){
          id
          bookId
        }
      }
    `
  )


  const startReadingAction = async () => {


    try {
      if(book?.id){
      await startReadingStore.mutate({ 
        input: { 
          bookId: book.id, 
          userId: 5 
        } 
      })
    }
    } catch (error) {
      console.error("Error",error)
    }

    
    goto("/")
  }
  

 
  



</script>

<section class="max-w-4xl mx-auto">
  {#if !isFetching && book}
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
    <!-- Header -->
    <div class="bg-linear-to-r from-blue-500 to-purple-600 text-white p-8">
      <h1 class="text-3xl font-bold mb-2">{book.title}</h1>
      {#if author}
        <p class="text-xl opacity-90">por {author.name}</p>
      {/if}
    </div>

    <!-- Book Info -->
    <div class="p-8">
      <div class="grid md:grid-cols-2 gap-8">
        <!-- Book Cover Placeholder -->
        <div class="flex justify-center">
          <div class="bg-linear-to-br from-blue-400 to-purple-600 w-64 h-96 rounded-lg shadow-xl flex items-center justify-center">
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

            {#if author}
              <div>
                <span class="font-medium text-gray-700">Autor:</span>
                <span class="ml-2">{author?.fullname ? author.fullname : author.name}</span>
               
                  <span class="text-gray-500">({author.country})</span>
                
              </div>
            {/if}
          </div>

          <!-- Actions -->
          <div class="pt-6 space-y-3">
            <button 
              onclick={startReadingAction}
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
  {:else}
    <progress  value="32" max="100"></progress> 
  {/if}
</section>

