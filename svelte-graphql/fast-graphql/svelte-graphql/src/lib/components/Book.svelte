<script lang="ts">
  import type { GetBooks$result } from "$houdini";
  type Book = GetBooks$result["books"][number]

  const  { book } : { book: Book}  = $props();


</script>


<div class="flex flex-col justify-between bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow w-52 max-h-4/5">
  <!-- Cover placeholder -->
  <div class="bg-linear-to-br from-blue-400 to-purple-600 h-64 flex items-center justify-center">
    <span class="text-white text-6xl">📖</span>
  </div>
  
  <!-- Info -->
  <div class="p-4">
    <h3 class="font-bold text-lg line-clamp-2 mb-2">{book.title}</h3>
    
    {#if book.author}
      <p class="text-sm text-gray-600 mb-2">{book.author.name}</p>
    {/if}
    
    <div class="flex justify-between text-xs text-gray-500">
      <span>{book.publicationYear}</span>
      <span>{book.pages} pág.</span>
    </div>
  </div>
  
  <!-- Footer actions -->
  <div class="px-4 pb-4">
    <a 
      href="/books/{book.id}" 
      class="block w-full text-center bg-green-600 text-white py-2 rounded hover:bg-green-700 transition mb-2 "
    >
     Ver detalles
    </a>
    <a 
      href="/books/{book.id}/chat"
      class="block w-full text-center underline hover:text-blue-500 transition"
    >Chat & Discuss</a>
  </div>
</div>
