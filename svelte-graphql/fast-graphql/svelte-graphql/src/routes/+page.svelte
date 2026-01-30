<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import { getContextClient } from "@urql/svelte";
  import { MY_READING_PROGRESS } from "$lib/graphql/queries";
  import Reading from "$lib/components/Reading.svelte";

  const userId = 'user123'
  const resultMyReadingProgress = queryStore({
    client: getContextClient(),
    query: MY_READING_PROGRESS,
    variables: {userId}
  });

  


</script>

{#if $resultMyReadingProgress.fetching}
  <div class="animate-pulse">Cargando...</div>
{:else if $resultMyReadingProgress.error}
  <div class="bg-red-100 text-red-700 p-4 rounded">
    Ouups: ha habido un error al obtener sus datos. Contacta con el equipo de soporte
  </div>
{/if}




{#if $resultMyReadingProgress?.data?.myReadingProgress}
  <h2 class="text-2xl font-bold mb-4">📖 Leyendo Actualmente</h2>
  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each $resultMyReadingProgress.data.myReadingProgress as reading (reading.id)}
      <Reading {reading} />
    {/each}
  </section>
{/if}



