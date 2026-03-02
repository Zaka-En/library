
<script lang="ts">
  import Spinner from "../ui/Spinner.svelte";
  import { RoomBookingController } from "./RoomBookingController.svelte";
  import { type ConferenceRoom } from "./types.ts";

  let {
    room,
    userId
  } : { 
    room: ConferenceRoom,
    userId: number
  }
  = $props()

  const DUPLICATE_ROOM_BOOKING_ERROR = "DUPLICATE_ROOM_BOOKING"

  const roomBookingController = new RoomBookingController(room, userId)

</script>

<div
  class="flex min-h-72 w-xs flex-col bg-[#dddacf] shadow-md rounded-2xlshadow-md font-normal p-2"
>
  {#if !roomBookingController.isLoadingBookRoom }
    <div class="mb-2 flex items-center justify-between px-4 pt-4">
      <h3 class="text-2xl font-semibold text-gray-800">{room?.name}</h3>
      <small class="text-az text-gray-400">Max: {room?.capacity}per</small>
    </div>

    <div class="mt-3 flex items-center justify-between px-4">
      <button
        onclick={() => {
          roomBookingController.moveBetweenDays(-1)
          roomBookingController.onChangeDay()
        }}
        disabled={roomBookingController.isToday}
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
      <span class="text-xs font-medium text-gray-600">{roomBookingController.dateLabel}</span>
      <button
        onclick={() => {
          roomBookingController.moveBetweenDays(1)
          roomBookingController.onChangeDay()
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
      {#if roomBookingController.availableHours.length === 0}
        <span class="text-sm text-gray-800 flex items-center justify-center flex-1 italic"
        >Agotado</span>
      {:else if !roomBookingController.isLoadingHours }
        <div class="mb-4 flex flex-wrap gap-1.5 px-4 overflow-y-scroll">
          {#each roomBookingController.availableHours as hour (hour)}
            <button 
              onclick={() => {roomBookingController.toggleHourButton(hour)}}
              class=" w-18 cursor-pointer rounded-full 
              pt-2 pb-2 text-xs hover:bg-green-400
              {roomBookingController.selectedHour === hour ? 'bg-green-400' : 'bg-green-200'}">{hour}:00
            </button>
          {/each} 
        </div>
      {:else}
        <div class="flex justify-center items-center">
          <Spinner size="45"/>
        </div>
      {/if}
        
    </div>

    {#if roomBookingController.selectedHour }
      <div class="flex flex-col gap-2 mx-auto mb-3">
        <label class="text-[12px] font-semibold" for="text">Número de personas que van a atender:</label>
        <input bind:value={roomBookingController.attendees} class="w-6/12 rounded-4xl h-6" type="number" name="attendees" id="attendees" max={room.capacity} min=1>
      </div>

      <div class="m-auto flex justify-center items-center mb-3">
        <button onclick={() => {roomBookingController.onConfirmHour()}} disabled={roomBookingController.isLoadingBookRoom}
        class="text-xs cursor-pointer rounded-full bg-amber-50 py-2 px-5 hover:bg-amber-100" >Confirmar</button>
      </div>
    {/if}
  
  {:else if roomBookingController.hasRequestedBookRoom}    
    <div class="flex flex-col items-center justify-center flex-1 gap-4 h-full">
      <button 
        onclick={()=>{roomBookingController.onBackToRoomBookHours()}}
        type="button"
        class="rounded-lg border border-gray-200 bg-gray-50 px-5 py-1.5 text-xs font-semibold text-gray-600 transition-all hover:bg-white hover:shadow-sm active:scale-95 cursor-pointer"
      >
        Volver
      </button>
      {#if roomBookingController.isBookRoomSuccess}  
        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="100" height="100" viewBox="0 0 128 128"
            style="fill:#40C057;">
            <path d="M 64 6 C 32 6 6 32 6 64 C 6 96 32 122 64 122 C 96 122 122 96 122 64 C 122 32 96 6 64 6 z M 64 12 C 92.7 12 116 35.3 116 64 C 116 92.7 92.7 116 64 116 C 35.3 116 12 92.7 12 64 C 12 35.3 35.3 12 64 12 z M 85.037109 48.949219 C 84.274609 48.974219 83.500391 49.300391 82.900391 49.900391 L 62 71.599609 L 51.099609 59.900391 C 49.999609 58.700391 48.100391 58.599219 46.900391 59.699219 C 45.700391 60.799219 45.599219 62.700391 46.699219 63.900391 L 59.800781 78 C 60.400781 78.6 61.1 79 62 79 C 62.8 79 63.599219 78.699609 64.199219 78.099609 L 87.199219 54 C 88.299219 52.8 88.299609 50.900781 87.099609 49.800781 C 86.549609 49.200781 85.799609 48.924219 85.037109 48.949219 z"></path>
        </svg>
        <div class="flex flex-col items-center gap-1">
          <span class="text-sm font-bold text-gray-800">Solicitado correctamente</span>
          <span class="text-xs text-gray-400 italic">Revisa tu correo</span>
        </div>
      {:else}
        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="100" height="100" viewBox="0 0 48 48">
          <linearGradient id="hbE9Evnj3wAjjA2RX0We2a_OZuepOQd0omj_gr1" x1="7.534" x2="27.557" y1="7.534" y2="27.557" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f44f5a"></stop><stop offset=".443" stop-color="#ee3d4a"></stop><stop offset="1" stop-color="#e52030"></stop></linearGradient><path fill="url(#hbE9Evnj3wAjjA2RX0We2a_OZuepOQd0omj_gr1)" d="M42.42,12.401c0.774-0.774,0.774-2.028,0-2.802L38.401,5.58c-0.774-0.774-2.028-0.774-2.802,0	L24,17.179L12.401,5.58c-0.774-0.774-2.028-0.774-2.802,0L5.58,9.599c-0.774,0.774-0.774,2.028,0,2.802L17.179,24L5.58,35.599	c-0.774,0.774-0.774,2.028,0,2.802l4.019,4.019c0.774,0.774,2.028,0.774,2.802,0L42.42,12.401z"></path><linearGradient id="hbE9Evnj3wAjjA2RX0We2b_OZuepOQd0omj_gr2" x1="27.373" x2="40.507" y1="27.373" y2="40.507" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#a8142e"></stop><stop offset=".179" stop-color="#ba1632"></stop><stop offset=".243" stop-color="#c21734"></stop></linearGradient><path fill="url(#hbE9Evnj3wAjjA2RX0We2b_OZuepOQd0omj_gr2)" d="M24,30.821L35.599,42.42c0.774,0.774,2.028,0.774,2.802,0l4.019-4.019	c0.774-0.774,0.774-2.028,0-2.802L30.821,24L24,30.821z"></path>
        </svg>
        <div class="flex flex-col items-center gap-1 text-sm text-gray-700">
          <span class="font-bold text-red-500">Lo lamentamos 😥</span>
          {#if roomBookingController.errorMsg === DUPLICATE_ROOM_BOOKING_ERROR}
            <span>la hora: {roomBookingController.selectedHour}:00 ya está reservada</span>
          {:else}
            <span>Hubo un error. <a class="text-blue-400 italic underline" href="/">Support team</a> </span>
          {/if}
          <span class="text-sm">Consulta otros horarios</span>          
        </div>
      {/if}
    </div>
  {:else}
    <div class=" justify-self-center self-center">
      <Spinner size="80"/>
    </div>   
  {/if}   
</div>