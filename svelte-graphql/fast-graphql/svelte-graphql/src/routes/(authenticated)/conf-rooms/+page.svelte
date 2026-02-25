<script lang="ts">
	import ConferenceRoom from "$lib/components/ConferenceRoom.svelte";
	import type { PageProps } from './$types';
	import { type ConferenceRoom$result } from "$houdini";
	

	type ConferenceRoom = ConferenceRoom$result["conferenceRooms"][number]

  const { data } : PageProps = $props()

	const conferenceRoomStore = $derived(data.conferenceRoomStore)
	const userId = $derived(data.user.id)
	$inspect(userId)
	let conferenceRooms: ConferenceRoom[]   = $derived($conferenceRoomStore.data?.conferenceRooms ?? [])

</script>

{#each conferenceRooms as conferenceRoom (conferenceRoom.id)}
	<ConferenceRoom room={conferenceRoom} {userId}/>
{/each}
