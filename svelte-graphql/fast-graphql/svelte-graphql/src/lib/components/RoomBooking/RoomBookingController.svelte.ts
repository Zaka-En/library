import { type ConferenceRoom } from "./types";
import dayjs from "dayjs";
import { graphql } from "$houdini"

const FIRST_AVAILABLE_HOUR = 9;

// Stores de Houdini (Sin el $ porque estamos en un .ts)
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

export class RoomBookingController {
  
  //TODO QUITAR STATE EN PRIVATE
  #room : ConferenceRoom;
  #userId: number;
  #lastQueryToken = 0;

  
  availableHours = $state<number[]>([]);
  currentDate = $state.raw(dayjs());
  selectedHour = $state<number | null>(null);
  attendees = $state<number | null>(null);
  
  
  isLoadingHours = $state(false); 
  isLoadingBookRoom = $state(false);
  isBookRoomSuccess = $state<boolean | null>(null);
  hasRequestedBookRoom = $state(false);
  errorMsg = $state("");

  constructor(room: ConferenceRoom, userId: number) {
    this.#room = room;
    this.#userId = userId;
    this.availableHours = room.availableHours ?? []; 

  }

  // Getters derivados 
  get isToday() { return this.currentDate.isSame(dayjs(), 'day'); }
  
  get dateLabel() {
    return this.isToday ? 'Hoy' : this.currentDate.format('DD/MM/YYYY');
  }

  moveBetweenDays = async (days: number) => {
    this.currentDate = this.currentDate.add(days, 'day');
    await this.onChangeDay();
  }

  onChangeDay = async () => {
    const queryToken = ++this.#lastQueryToken;
    this.selectedHour = null;
    this.isLoadingHours = true;

    let startingHour = this.isToday ? (dayjs().hour() + 1) : FIRST_AVAILABLE_HOUR;
    
    // Al usar .fetch() obtenemos el resultado directamente
    const result = await getAvailableHoursStore.fetch({
      variables: {
        roomId: Number(this.#room?.id),
        date: this.currentDate.format('YYYY-MM-DD'),
        startingHour
      },
      policy: 'NetworkOnly',
    });

    if (queryToken !== this.#lastQueryToken) return;

    this.availableHours = result.data?.availableHours ?? [];
    this.isLoadingHours = false;
  }

  onConfirmHour = async () => {
    if (!this.selectedHour || this.isLoadingBookRoom) return;

    this.isLoadingBookRoom = true;
    
    const { errors } = await bookRoomStore.mutate({
      input: {
        roomId: Number(this.#room?.id),
        attendeesCount: this.attendees || 1,
        userId: this.#userId,
        date: this.currentDate.format('YYYY-MM-DD'),
        hour: this.selectedHour
      }
    });

    this.hasRequestedBookRoom = true;
    this.attendees = null;
    this.isLoadingBookRoom = false;

    if (errors) {
      this.isBookRoomSuccess = false;
      this.errorMsg = errors[0].message;
    } else {
      this.isBookRoomSuccess = true;
    }
  }

  toggleHourButton = (hour: number) => {
    this.selectedHour = this.selectedHour === hour ? null : hour;
  }

  onBackToRoomBookHours = async () => {
    await this.onChangeDay() // refresh room booking availablehours
    this.hasRequestedBookRoom=false
    this.isLoadingBookRoom=false
  }
}

