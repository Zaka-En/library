<script lang="ts">
  import { graphql } from "$houdini";
  import { SvelteSet } from "svelte/reactivity";
  import { onMount } from "svelte";

  import client from "../../client";

  console.log(client.plugins)
  
  const ratingStore = graphql(`
    subscription BookRatings{
      bookRatings
    }
  `);

  onMount(()=>{
    ratingStore.listen()

    return () => {
      ratingStore.unlisten()
    }
  })
  

  let persistedRatings: SvelteSet<string> = $state(new SvelteSet())
  let currentRating = $derived($ratingStore.data?.bookRatings)

  $effect(() =>{
    console.log("Valor actual del store:", $ratingStore.data);
    if (currentRating) {
      persistedRatings.add(currentRating)
    }    
  })

  

  $inspect(persistedRatings.entries())
  
</script>

<section class="flex flex-col gap-3">
  {#if currentRating}
    <h2>ÚLTIMA VALORACIÓN: {currentRating}</h2>
  {/if}

  <ul>
    {#each persistedRatings as rating}
      <li>{rating}</li>
    {/each}
  </ul>

  <p class=" text-blue-700">Estado: {$ratingStore.fetching ? 'Conectado...' : 'Esperando...'}</p>
</section>