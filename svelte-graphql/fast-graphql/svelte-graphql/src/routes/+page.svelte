<script lang="ts">
  import { queryStore, gql } from "@urql/svelte";
  import { client } from "$lib/graphql/client";
  import { getContextClient } from "@urql/svelte";

  const authorsQuery = gql`
    query{
      authors{
        id
        name
      }
    }
  `;

  const result = queryStore({
    client: getContextClient(),
    query: authorsQuery
  });



</script>


{#if $result.fetching}
  <p>Loading...</p>
{:else if $result.error}
  <pre>{$result.error.message}</pre>
{:else}
  <pre>{JSON.stringify($result.data, null, 2)}</pre>
{/if}



