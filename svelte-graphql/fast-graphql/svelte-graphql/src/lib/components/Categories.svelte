<script lang="ts">
  

  let { categories, categorySnippet, children} = $props();
</script>

<aside class=" w-3/12 h-auto flex flex-col gap-2">
  {@render children()}
  {#each categories as cat}
    <div class="group bg-white p-4 rounded-lg border border-gray-100 ">
      {@render categorySnippet(cat.name, cat.description, cat.totalBooks)}
    </div>
  {/each}
</aside>
