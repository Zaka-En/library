<script lang="ts">
  import AuthorsList from "$lib/components/AuthorsList.svelte";
  let { data } = $props();
  
</script>

<section>
  <div class="flex justify-between items-center mb-7">
    <h1 class="text-3xl font-bold">Autores</h1>
    <a
      href="/authors/new"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
    >
      + Nuevo Autor
    </a>
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2">
    <AuthorsList authors={data.authors} />
  </div>
</section>
