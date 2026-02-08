<script lang="ts">
  import type { PageInfo } from "$houdini";
  import { onMount } from "svelte";

  interface Props {
    pageInfo: PageInfo;
    fetching: boolean;
    onNext: (cursor: string | null) => void;
    onPrevious: (cursor: string | null) => void;
    itemsPorPage?: number;
  }

  let {
    pageInfo,
    fetching = false,
    onNext,
    onPrevious,
    itemsPorPage = 5,
  }: Props = $props();
 
  

  
  const totalPages = $derived(Math.ceil(pageInfo?.totalCount / itemsPorPage));
  let endCursor = $derived(pageInfo.endCursor ?? "");
  let decodedEndCursor = $derived(endCursor ? Number(atob(endCursor).split(':').at(-1)) : 1);
  let currentPage = $derived( Math.ceil(decodedEndCursor/itemsPorPage));

  
</script>

<div class="flex gap-4 justify-between items-center w-40">
  <button
    onclick={() => {
      onPrevious(pageInfo.startCursor);
    }}
    disabled={!pageInfo.hasPreviousPage || fetching}
    class="w-8 h-8 flex items-center justify-center rounded-full bg-white shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
    aria-label="Atrás"
  >
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M15 19l-7-7 7-7"
      />
    </svg>
  </button>

  <div class="w-16 h-8 flex justify-center items-center border border-black ">
    {#if !isNaN(totalPages)}
      <span class="text-center w-8">{currentPage}</span>/
      <span class="text-center w-8">{totalPages}</span>
    {/if}
  </div>

  <button
    onclick={() => {
      onNext(pageInfo.endCursor);
    }}
    disabled={!pageInfo.hasNextPage || fetching}
    class="w-8 h-8 flex items-center justify-center rounded-full bg-white shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
    aria-label="Adelante"
  >
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M9 5l7 7-7 7"
      />
    </svg>
  </button>
</div>
