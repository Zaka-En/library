export interface BaseRoom {
	id: number | string;
	name: string;
	capacity: number;
	availableHours?: number[];
}

export interface BookingRoomProvider<TRoom extends BaseRoom> {
	getAvailableHours: (room: TRoom, date: string, startingHour: number) => Promise<number[]>;
	bookRoom: (input: any) => Promise<{ success: boolean; error?: string }>;
}
