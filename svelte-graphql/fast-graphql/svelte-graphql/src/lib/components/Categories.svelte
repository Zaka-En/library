<script lang="ts">

  import type { Snippet } from "svelte";

  interface Props{
    categories: CategoryType[]
    categorySnippet: Snippet<[string,string,number]>
    children: Snippet<[CategoryType|undefined,Snippet<[string,string,number]>]>
  }
  

  let { categories, categorySnippet, children} : Props = $props();
  


</script>

<aside class=" w-3/12 h-auto flex flex-col gap-2">
   
  {#if children}
    {#each categories as cat }
      {@render children(cat,categorySnippet)}
    {/each}
  {:else}
	  <p>fallback content</p>
  {/if}
  
  
  
  <!-- {#each categories as cat}
    <div class="group bg-white p-4 rounded-lg border border-gray-100 ">
      {@render categorySnippet(cat.name, cat.description, cat.totalBooks)}
    </div>
  {/each} -->
</aside>
