<script lang="ts">
  import BookForm from "$lib/components/BookForm.svelte";
  import type { PageProps } from "./$types";

  let { data } : PageProps = $props()
  let event = $derived( data.event)
</script>

<BookForm {event}  />