import type { PageLoad } from './$types';
import { graphql } from '$houdini';
import dayjs from 'dayjs';

const conferenceRoomStore = graphql(`
  query ConferenceRooms($startingHour: Int!) {
    conferenceRooms {
      id
      name
      capacity
      availableHours(startingHour: $startingHour)
    }
  }
`)

export const load: PageLoad = async (event) => {

  let startingHour = dayjs().hour() + 1

  await conferenceRoomStore.fetch({
    event,
    variables: { startingHour }
  })

  return{
    conferenceRoomStore
  }
}