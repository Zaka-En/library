<script lang="ts">
  import AuthorForm from "$lib/components/AuthorForm.svelte";

  let { data } = $props()
</script>

<AuthorForm author={data.author}/>