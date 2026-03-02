import { type BaseRoom, type BookingRoomProvider } from "./types.ts";
import dayjs from 'dayjs'
const DEFAULT_STARTING_HOUR = 9

export class RoomBookingController<TRoom extends BaseRoom> {
  
  //TODO QUITAR STATE EN PRIVATE
  #room : TRoom;
  #userId: number;
  #provider: BookingRoomProvider<TRoom>
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

  constructor(
    room: TRoom,
    userId: number,
    provider: BookingRoomProvider<TRoom>) {
    this.#room = room;
    this.#userId = userId;
    this.availableHours = room.availableHours ?? []; 
    this.#provider = provider
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

    let startingHour = this.isToday ? (dayjs().hour() + 1) : DEFAULT_STARTING_HOUR;
    
    try {
      const hours = await this.#provider.getAvailableHours(
        this.#room,
        this.currentDate.format('YYYY-MM-DD'),
        startingHour
      )

      if (queryToken !== this.#lastQueryToken) return;

      this.availableHours = hours
    } catch (error) {
      this.errorMsg = "ERROR_LOADING_AVAILABLE_HOURS"
    } finally{
      this.isLoadingHours = false;
    }
    
  }


  // the developer(the user of the library) decides how to implement the TInput
  onConfirmHour = async () => {
    if (!this.selectedHour || this.isLoadingBookRoom) return;

    this.isLoadingBookRoom = true;

    const input ={
      roomId: Number(this.#room.id),
      userId: this.#userId,
      date: this.currentDate.format('YYYY-MM-DD'),
      hour: this.selectedHour,
      attendeesCount: this.attendees || 1
    }
    
    const { success, error } = await this.#provider.bookRoom(input)

    this.hasRequestedBookRoom = true;
    this.attendees = null;
    this.isLoadingBookRoom = false;

    this.isBookRoomSuccess = success
    this.errorMsg = error ?? ""
    this.hasRequestedBookRoom = true
    this.isLoadingBookRoom = false
   
    
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

