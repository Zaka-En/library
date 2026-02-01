<script lang="ts">
  const { reading, onUpdate, onFinish } = $props<{
    reading: any;
    onUpdate?: (book: any, reading: any) => void;
    onFinish?: (book: any, reading: any) => void;
  }>();

  const progress = $derived(
    reading?.book?.pages > 0
      ? Math.round((reading.currentPage / reading.book.pages) * 100)
      : 0,
  );
</script>

<div class="bg-white shadow rounded-lg p-6 mb-4">
  <h3 class="text-xl font-semibold">
    {reading.book.title}
  </h3>

  <p class="text-gray-600">
    {reading.book.author.name}
  </p>

  <div class="mt-4">
    <div class="flex justify-between text-sm mb-1">
      <span>
        {reading.currentPage} / {reading.book.pages} páginas
      </span>
      <span>{progress}%</span>
    </div>

    <div class="w-full bg-gray-200 rounded-full h-2">
      <div
        class="bg-blue-600 h-2 rounded-full transition-all"
        style="width: {progress}%"
      ></div>
    </div>
  </div>

  <!-- Action Buttons -->
  <div class="mt-4 flex gap-2">
    {#if !reading.finishDate}
      <button
        onclick={() => onUpdate?.(reading.book, reading)}
        class="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition text-sm font-medium"
      >
        📖 Actualizar Progreso
      </button>
      
      <button
        onclick={() => onFinish?.(reading.book, reading)}
        class="flex-1 bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 transition text-sm font-medium"
      >
        ✅ Finalizar Lectura
      </button>
    {:else}
      <div class="flex-1 bg-green-100 text-green-800 py-2 px-4 rounded text-center text-sm font-medium">
        🎉 ¡Completado!
      </div>
    {/if}
  </div>
</div>
