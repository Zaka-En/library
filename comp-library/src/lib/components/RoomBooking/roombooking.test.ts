import { RoomBookingController } from './RoomBookingController.svelte.ts';
import { describe, it, expect, vi, beforeEach, test } from 'vitest';
import dayjs from 'dayjs';

const mockRoom = { id: 1, name: 'Sala A', capacity: 10 };

const mockProvider = {
	getAvailableHours: vi.fn(), // in this case vi mocks a function
	bookRoom: vi.fn()
};
// in this case vi mocks a function
beforeEach(() => {
	vi.clearAllMocks();
});

// describe groups all logically related tests
describe('onChangeDay', () => {
	it('Loads available hours correctly', async () => {
		mockProvider.getAvailableHours.mockResolvedValue([9, 10, 11]);
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		await ctrl.onChangeDay();
		expect(ctrl.availableHours).toEqual([9, 10, 11]);
		expect(ctrl.isLoadingHours).toBe(false);
	});

	it('Resets selectedHour after changing day', async () => {
		mockProvider.getAvailableHours.mockResolvedValue([9]);
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		ctrl.selectedHour = 9;
		await ctrl.onChangeDay();

		expect(ctrl.selectedHour).toBeNull();
	});

	it('Sets errMsg if call is failed', async () => {
		mockProvider.getAvailableHours.mockRejectedValue(new Error('ERROR WHILE LOADING'));
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		await ctrl.onChangeDay();

		expect(ctrl.errorMsg).toEqual('ERROR_LOADING_AVAILABLE_HOURS');
		expect(ctrl.isLoadingHours).toBeFalsy();
	});

	it('Ignores old query responses (race condition)', async () => {
		mockProvider.getAvailableHours.mockResolvedValueOnce([9]).mockResolvedValueOnce([10, 12]);

		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		const first = ctrl.onChangeDay(); // [9]
		const second = ctrl.onChangeDay(); // [10,12]

		await Promise.all([first, second]);

		expect(ctrl.availableHours).toEqual([10, 12]);
	});
});

describe('moveBetweenDays', () => {
	it('Day changes correctly', async () => {
		mockProvider.getAvailableHours.mockResolvedValue([]);
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		await ctrl.moveBetweenDays(-221);
		expect(ctrl.currentDate.date()).toEqual(dayjs().add(-221, 'day').date());
		expect(ctrl.currentDate.month()).toEqual(dayjs().add(-221, 'day').month());
	});
});

describe('Confirming a booking hour', () => {
	it('Nothing happens when no hour is selected', async () => {
		mockProvider.bookRoom.mockResolvedValue({});
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		ctrl.selectedHour = null;
		await ctrl.onConfirmHour();

		expect(mockProvider.bookRoom).not.toHaveBeenCalled();
	});

	it('Nothing happens when loading for previous confimation', async () => {
		mockProvider.bookRoom.mockResolvedValue({});
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		ctrl.isLoadingBookRoom = true;
		await ctrl.onConfirmHour();

		expect(mockProvider.bookRoom).not.toHaveBeenCalled();
	});

	it('Confirmation of Booking Room is Successful', async () => {
		mockProvider.bookRoom.mockResolvedValue({ success: true });
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		ctrl.selectedHour = 12;
		ctrl.attendees = 11;

		await ctrl.onConfirmHour();

		expect(ctrl.isBookRoomSuccess).toBeTruthy();
		expect(ctrl.errorMsg).toEqual('');
		expect(ctrl.hasRequestedBookRoom).toBeTruthy();
		expect(ctrl.attendees).toBeNull();
		expect(ctrl.isLoadingBookRoom).toBeFalsy();
	});

	it('Confirmation of Booking Room has failed', async () => {
		mockProvider.bookRoom.mockResolvedValue({ success: false, error: 'Error' });
		const ctrl = new RoomBookingController(mockRoom, 1, mockProvider);

		ctrl.selectedHour = 12;
		ctrl.attendees = 11;

		await ctrl.onConfirmHour();

		expect(ctrl.isBookRoomSuccess).toBeFalsy();
		expect(ctrl.errorMsg).toEqual('Error');
		expect(ctrl.hasRequestedBookRoom).toBeTruthy();
		expect(ctrl.attendees).toBeNull();
		expect(ctrl.isLoadingBookRoom).toBeFalsy();
	});
});
