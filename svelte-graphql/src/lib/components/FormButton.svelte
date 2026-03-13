<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props{
    loading?: boolean
    isEdit?: boolean
    submitSnippet?: Snippet<[boolean | undefined, boolean | undefined]>
    [key: string] : any
  }

  let {
    loading = false,
    isEdit = false,
    submitSnippet,
    ...rest
  } : Props = $props()

  

</script>


<button
  type= "submit"
  disabled={loading} 
  {...rest}
  
>
  {#if submitSnippet}
    {@render submitSnippet(loading,isEdit)}
  {:else}
    <span>Default submit Button</span>
  {/if}
</button>   
