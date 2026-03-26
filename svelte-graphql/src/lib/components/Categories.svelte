<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    categories: CategoryType[];
    categorySnippet: Snippet<[string, string, number]>;
    children: Snippet<[CategoryType, Snippet<[string, string, number]>]>;
  }

  let { categories, categorySnippet, children }: Props = $props();
</script>

<aside class="w-3/12 h-auto flex flex-col gap-2">
  {#if children}
    {#each categories as cat}
      <div class="category-card">
        {@render children(cat, categorySnippet)}
      </div>
    {/each}
  {:else}
    <p>fallback content</p>
  {/if}
</aside>
