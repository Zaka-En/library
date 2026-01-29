<script lang="ts">
  const { reading } = $props();

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
</div>
