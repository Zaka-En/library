<script lang="ts">
  import { goto } from "$app/navigation";
  import AuthorForm from "$lib/components/AuthorForm.svelte";
  import type { LayoutProps } from "../$types";
  let { data }: LayoutProps = $props();

  //this Author interface is for houdini
  interface Author {
    readonly id: string;
    readonly name: string;
    readonly biography: string | null;
    readonly country: string;
    readonly fullname: string | null;
  }

  let authorStore = $derived(data.store);
  let author = $derived($authorStore.data?.author) as Author;

  function handleSuccess() {
    goto("/authors");
  }
</script>

<AuthorForm {author} onSuccess={handleSuccess} />
