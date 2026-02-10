<script lang="ts">

  import "./layout.css";
  const { children } = $props()

</script>

<header
  class="w-full h-20 flex justify-between items-center fixed top-0 left-0 px-5 bg-black/5"
>
  <h2 class=" font-bold text-3xl">Mi Biblioteca</h2>
  <nav class="flex gap-4">
		<a class=" inline-block p-1 hover:underline transition" href="/">Inicio</a>
    <a class=" inline-block p-1 hover:underline transition" href="/authors">Autores</a>
    <a class=" inline-block p-1 hover:underline transition" href="/books">Libros</a>
    <a class=" inline-block p-1 hover:underline transition" href="/ratings">Valoraciones</a>
  </nav>
</header>

<main class='container flex  justify-between mx-auto px-4 py-8 max-w-7xl mt-20'>
	{@render children?.()}
</main>


