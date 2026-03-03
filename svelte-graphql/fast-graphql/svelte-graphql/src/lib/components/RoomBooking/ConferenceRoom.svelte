
<script lang="ts">

  import { RoomBooker, type BookingRoomProvider } from '@fast-svelte-graphql/comp-library'
  import { type ConferenceRoom } from "./types.ts";
  import { graphql } from '$houdini';

  const getAvailableHoursStore = graphql(`
    query AvailableHours($roomId: Int!, $date: String!, $startingHour: Int!){
      availableHours(roomId: $roomId, date: $date, startingHour: $startingHour )
    }
  `);

  const bookRoomStore = graphql(`
    mutation BookRoom($input: RoomBookingInput!){
      bookConferenceRoom(input: $input){
        roomId hour date attendeesCount
      }
    }
  `);


  let {
    room,
    userId,
  } : { 
    room: ConferenceRoom,
    userId: number
  }
  = $props()

  //const DUPLICATE_ROOM_BOOKING_ERROR = "DUPLICATE_ROOM_BOOKING"

  const houdiniRoomBookingProvider: BookingRoomProvider<ConferenceRoom> = {
    getAvailableHours: async (room, date, startingHour) => {
      const result = await getAvailableHoursStore.fetch({
        variables: { roomId: Number(room.id), date, startingHour }
      });
      return result.data?.availableHours ?? [];
    },
    bookRoom: async (input) => {
      const { data, errors } = await bookRoomStore.mutate({ input });
      return { 
        success: !errors, 
        error: errors?.[0].message 
      };
    }
  }

</script>


<RoomBooker 
  {room}
  {userId}
  provider={houdiniRoomBookingProvider}
 />