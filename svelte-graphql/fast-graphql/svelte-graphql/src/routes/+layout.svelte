<script lang="ts">
  import { setContextClient } from '@urql/svelte';
  import { client } from '$lib/graphql/client';

  setContextClient(client);
</script>

<slot />
