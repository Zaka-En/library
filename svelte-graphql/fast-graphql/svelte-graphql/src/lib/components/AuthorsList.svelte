<script lang="ts">
  const { authors } = $props();
</script>

{#if authors}
  {#each authors as author (author.node.id)}
    <div class="bg-white shadow rounded-lg p-6 mb-5 mx-2">
      <div class="flex justify-between items-start">
        <div>
          <h2 class="text-xl font-semibold">{author.node.name}</h2>
          <p class="text-gray-600 text-sm">🌍 {author.node.country}</p>
          <p class="text-gray-700 mt-2">
            {author.node?.biography?.slice(0, 100)}...
          </p>
        </div>
        <div class="flex gap-2">
          <a href="/authors/{author.node.id}" class="text-blue-600 hover:underline"
            >Ver</a
          >
          <a
            href="/authors/{author.node.id}/edit"
            class="text-gray-600 hover:underline">Editar</a
          >
        </div>
      </div>
    </div>
  {/each}
{:else}
  <div>No hay ningún autor registrado</div>
{/if}
