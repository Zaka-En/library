<script module lang="ts">
    import { goto } from "$app/navigation";
  import { graphql, type ConferenceRoom$result } from "$houdini";
	type ConferenceRoom = ConferenceRoom$result["conferenceRooms"][number]
  
</script>

<script lang="ts">
  import { type BookRoom$input } from "$houdini";
  import dayjs from "dayjs";
  let {room, userId}: { room: ConferenceRoom, userId: number } = $props()
  let availableSlots= $state(room.availableSlots ?? [])
  let currentDate = $state.raw(dayjs());
  let dateLable = $derived(
    currentDate.isSame(dayjs(),'day')
    ? 'Hoy'
    : currentDate.format('DD/MM/YYYY')
  )
  let selectedHour: number | null = $state(null) 
  let isLoading = $state(false)
  let attendees: number | null = $state(null)


  const getAvailableSlotsStore = graphql(`
    query AvailableSlotes($roomId: Int!, $date: String!){
      availableSlots(roomId: $roomId, date: $date)
    }
  `)

  const bookRoomStore = graphql(`
    mutation BookRoom($input: RoomBookingInput!){
      bookConferenceRoom(input: $input){
        roomId
        startHour
        endHour
      }
    }
  `)

  $effect(() => {
    if (availableSlots) {
      selectedHour = null
    }
  })
  

  let availableHours= $derived.by(() => {
    const hours: number[] = []
    availableSlots.forEach(slot => {
      let startHour = slot[0]
      let endHour = slot[1]
      while (endHour>startHour) {
        hours.push(startHour)
        startHour++
      }
    });

    return hours
  })

  const moveBetweenDays = (days: number) => {
    currentDate = currentDate.add(days, 'day')
  }

  const onChangeDay = async () => {
    await getAvailableSlotsStore.fetch({variables:{roomId: Number(room.id), date: currentDate.format('YYYY-MM-DD')}})
    const newAvailableSlots = $getAvailableSlotsStore.data?.availableSlots ?? []
    availableSlots = newAvailableSlots // <-- Aquí estoy haciendo un reassignment
  }

  const onConfirmHour = async () => {
    if(!selectedHour) return

    const input: BookRoom$input = {
      input:{
        roomId: Number(room.id),
        attendeesCount: attendees || 1,
        userId: userId, // hardcoded para probar
        date: currentDate.format('YYYY-MM-DD'),
        startHour: selectedHour,
        endHour: selectedHour + 1
      }
    }
    
    const result = await bookRoomStore.mutate(input)

    if(result.data){
      goto("/")
    }
  }

</script>

<div
  class="flex min-h-72 w-xs flex-col bg-white shadow-md rounded-2xlshadow-md font-normal p-2 "
>
  <div class="mb-2 flex items-center justify-between px-4 pt-4">
    <h3 class="text-2xl font-semibold text-gray-800">{room?.name}</h3>
    <small class="text-az text-gray-400">Max: {room?.capacity}per</small>
  </div>

  <div class="mt-3 flex items-center justify-between px-4">
    <button
      onclick={() => {
        moveBetweenDays(-1)
        onChangeDay()
      }}
      disabled={currentDate.isSame(dayjs(),'day')}
      aria-label="Previous"
      class="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-50 transition hover:bg-amber-100 cursor-pointer disabled:cursor-not-allowed "
    >
      <svg
        class="h-4 w-4 text-gray-500"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M15 19l-7-7 7-7"
        />
      </svg>
    </button>
    <span class="text-xs font-medium text-gray-600">{dateLable}</span>
    <button
      onclick={() => {
        moveBetweenDays(1)
        onChangeDay()
      }}
      aria-label="Next"
      class="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-50 transition hover:bg-amber-100 cursor-pointer"
    >
      <svg
        class="h-4 w-4 text-gray-500"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>

 
  <div class="mt-5 mb-4 flex flex-col gap-3 px-4">
    <span class="text-center text-sm font-semibold text-gray-800"
      >Horarios disponibles</span
    >
    <!-- Este div entero es reactivo  -->
    <div class="mb-4 flex flex-wrap gap-1.5 px-4 overflow-y-scroll">
      {#each availableHours as hour (hour)}
        <button 
          onclick={() => {selectedHour=hour}}
          class=" w-18 cursor-pointer rounded-full 
           pt-2 pb-2 text-xs hover:bg-green-400
           {selectedHour === hour ? 'bg-green-400' : 'bg-green-200'}">{hour}:00
        </button>
      {/each} 
    </div>
  </div>

  {#if selectedHour }
    <div class="flex flex-col gap-2 mx-auto mb-3">
      <label class="text-[12px] font-semibold" for="text">Número de personas que van a atender:</label>
      <input bind:value={attendees} class="w-6/12 rounded-4xl h-6" type="number" name="attendees" id="attendees" max={room.capacity} min=1>
    </div>

    <div class="m-auto flex justify-center items-center mb-3">
      <button onclick={() => {onConfirmHour()}}
       class="text-xs cursor-pointer rounded-full bg-amber-50 py-2 px-5 hover:bg-amber-100" >Confirmar</button>
    </div>
  {/if}

  
</div>
