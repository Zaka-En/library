<script lang="ts">
	import ConferenceRoom, { type ConferenceRoom as ConferenceRoomType } from "$lib/components/ConferenceRoom.svelte";
	import type { PageProps } from './$types';


  const { data } : PageProps = $props()

	const conferenceRoomStore = $derived(data.conferenceRoomStore)
	const userId = $derived(data.user.id)
	$inspect(userId)
	let conferenceRooms: ConferenceRoomType[] = $derived($conferenceRoomStore.data?.conferenceRooms ?? [])

</script>

<section class="flex justify-center flex-wrap gap-4 mx-10 items-start">
	{#each conferenceRooms as conferenceRoom (conferenceRoom.id)}
		<ConferenceRoom room={conferenceRoom} {userId}/>
	{/each}
</section>

