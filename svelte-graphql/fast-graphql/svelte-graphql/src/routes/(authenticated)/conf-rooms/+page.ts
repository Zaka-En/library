import type { PageLoad } from './$types';
import { graphql } from '$houdini';

const conferenceRoomStore = graphql(`
  query ConferenceRoom {
    conferenceRooms {
      id
      name
      capacity
      availableSlots
    }
  }
`)

export const load: PageLoad = async (event) => {

  await conferenceRoomStore.fetch({event})

  return{
    conferenceRoomStore
  }
}