<script lang="ts">
	import ConferenceRoom from '$lib/components/RoomBooking/ConferenceRoom.svelte';
	import type { PageProps } from './$types';

	import { type ConferenceRooms$result } from "$houdini";

	type ConferenceRoomType = ConferenceRooms$result["conferenceRooms"][number]


  const { data } : PageProps = $props()

	const conferenceRoomStore = $derived(data.conferenceRoomStore)
	const userId = $derived(data.user?.id)
	$inspect(userId)
	let conferenceRooms: ConferenceRoomType[] = $derived($conferenceRoomStore.data?.conferenceRooms ?? [])

</script>

<section class="flex justify-center flex-wrap gap-4 mx-10 items-start">
	{#each conferenceRooms as conferenceRoom (conferenceRoom.id)}
		<ConferenceRoom room={conferenceRoom} {userId}/>
	{/each}
</section>

