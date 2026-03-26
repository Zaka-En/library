import { expect, vi, beforeEach, test } from 'vitest';
import { render } from 'vitest-browser-svelte';
import { page } from 'vitest/browser';
import RoomBooker from './RoomBooker.svelte';
import { tick } from 'svelte';

const mockRoom = { id: 1, name: 'Sala A', capacity: 10 };

const mockProvider = {
	getAvailableHours: vi.fn(), // in this case vi mocks a function
	bookRoom: vi.fn()
};

beforeEach(() => {
	vi.clearAllMocks();
});

test('First test of the component', async () => {
	mockProvider.getAvailableHours.mockResolvedValue([9, 10, 11]);
	mockProvider.bookRoom.mockResolvedValue({ success: true });

	const { baseElement } = render(RoomBooker, {
		room: mockRoom,
		userId: 1,
		provider: mockProvider
	});

	const screen = page.elementLocator(baseElement);

	const button9 = screen.getByRole('button', { name: /9:00/i });
	await expect.element(button9).toBeVisible();
	await button9.click();

	const confirmButton = screen.getByRole('button', { name: /Confirmar/i });
	await expect.element(confirmButton).toBeVisible();
	await confirmButton.click();

	await tick();
	await new Promise((r) => setTimeout(r, 100));

	await expect.element(screen.getByText('Revisa tu correo')).toBeVisible();
});

test('Manage race Condition with 11 clicks to next buttons', async () => {
	mockProvider.getAvailableHours.mockImplementation(async () => {
		await new Promise((r) => setTimeout(r, 200)); // Pequeño delay
		return [9];
	});

	mockProvider.getAvailableHours.mockResolvedValueOnce([10, 11]);

	const { baseElement } = render(RoomBooker, {
		room: mockRoom,
		userId: 1,
		provider: mockProvider
	});

	const screen = page.elementLocator(baseElement);
	const nextButton = screen.getByRole('button', { name: /next/i });

	for (let i = 0; i < 11; i++) {
		await nextButton.click();
	}

	await expect
		.poll(() => {
			const buttons = screen.getByRole('button', { name: /:00/i }).all();
			return buttons.length;
		})
		.toBe(2);

	await expect.element(screen.getByText('10:00')).toBeVisible();
	await expect.element(screen.getByText('11:00')).toBeVisible();
});

test('Previous day button disabled if the day is Today', async () => {
	mockProvider.getAvailableHours.mockResolvedValue([9, 10, 11]);
	mockProvider.bookRoom.mockResolvedValue({ success: true });

	const { baseElement } = render(RoomBooker, {
		room: mockRoom,
		userId: 1,
		provider: mockProvider
	});

	const screen = page.elementLocator(baseElement);
	const previousButton = screen.getByRole('button', { name: /previous/i });

	await expect.element(screen.getByText(/hoy/i)).toBeVisible();
	await expect.element(previousButton).toBeDisabled();
});
