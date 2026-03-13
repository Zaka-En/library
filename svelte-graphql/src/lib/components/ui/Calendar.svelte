<script lang="ts">
	import { type Dayjs } from "dayjs";
	import dayjs from "dayjs";
	import { onMount } from "svelte";

	let currentFirstDateOfMonth = $state.raw(dayjs().set("date", 1));
	let currentMonth = $derived(currentFirstDateOfMonth.month());
	let currentSpanishMonthName = $derived(convertToSpanishMonth(currentMonth));
	let currentDayNumber = $derived(currentFirstDateOfMonth.get("d"));
	let currentYear = $derived(currentFirstDateOfMonth.year());
	let days: Dayjs[] = $state([]);
	let selectedDate: Dayjs | null = $state(null);
	const isToday = (day: Dayjs) => {
		return day.isSame(dayjs(),'day')
	}

	function convertToSpanishMonth(month: number): string {
		const meses = [
			"Enero",
			"Febrero",
			"Marzo",
			"Abril",
			"Mayo",
			"Junio",
			"Julio",
			"Agosto",
			"Septiembre",
			"Octubre",
			"Noviembre",
			"Diciembre",
		];

		return meses[month];
	}

	onMount(() => {
		days = getDays();
	});

	const onChangeMonth = (isNext: boolean) => {
		if (isNext) {
			currentFirstDateOfMonth = currentFirstDateOfMonth.add(1, "month");
		} else {
			currentFirstDateOfMonth = currentFirstDateOfMonth.subtract(1, "month");
		}

		days = getDays();
	};

	//return all the 42 days to be displayed on the screnn
	function getDays() {
		let nPreviousDaysToTheFirst =
			currentDayNumber === 0 ? 6 : currentDayNumber - 1;
		let nRestOftheDays = 42 - nPreviousDaysToTheFirst;

		const resultDays: Dayjs[] = [];
		resultDays.push(currentFirstDateOfMonth);

		if (nPreviousDaysToTheFirst !== 0) {
			for (let i = 1; i <= nPreviousDaysToTheFirst; i++) {
				resultDays.unshift(currentFirstDateOfMonth.subtract(i, "day"));
			}
		}

		for (let i = 1; i < nRestOftheDays; i++) {
			resultDays.push(currentFirstDateOfMonth.add(i, "day"));
		}

		return resultDays;
	}
</script>

<section class="w-full max-w-xs aspect[7/6] border border-gray-500 rounded-xl p-2">
	<div class="h-full flex flex-col items-center">
		<div class="w-full h-14 flex justify-between items-center">
			<button
				onclick={() => {
					onChangeMonth(false);
				}}
				aria-label="Previous Month"
				class="px-2 cursor-pointer"
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
			<div class="h-full flex gap-1 items-center">
				<span class="text-lg font-semibold">{currentSpanishMonthName}</span>
				<span class="text-lg font-semibold">{currentYear}</span>
			</div>
			<button
				onclick={() => {
					onChangeMonth(true);
				}}
				aria-label="Next Month"
				class="px-2 cursor-pointer"
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
						d="M9 5l7 7-7 7"
					/>
				</svg>
			</button>
		</div>
		<div class="w-full grid grid-cols-7 justify-items-center gap-2">
			<span class="size-10 flex justify-center items-center">L</span>
			<span class="size-10 flex justify-center items-center">M</span>
			<span class="size-10 flex justify-center items-center">X</span>
			<span class="size-10 flex justify-center items-center">J</span>
			<span class="size-10 flex justify-center items-center">V</span>
			<span class="size-10 flex justify-center items-center">S</span>
			<span class="size-10 flex justify-center items-center text-red-500"
				>D</span
			>
		</div>
		<div
			class="w-full grid grid-cols-7 grid-rows-6 h-full justify-items-center gap-2"
		>
			{#key currentFirstDateOfMonth.format("YYYY-MM-DD")}			
				{#each days as day }
					{@const isSunday = day.day() === 0}
					{@const isDayOftheMonth =
						day.month() === currentFirstDateOfMonth.month()}
					{@const canBeSelected = !isSunday && isDayOftheMonth}
					<label
						class="w-full aspect-square flex justify-center items-center rounded-sm {!isDayOftheMonth
							? 'text-gray-300'
							: isSunday
								? 'text-red-500'
								: 'text-gray-800'}
						{canBeSelected ? 'hover:border border-gray-600 cursor-pointer ' : ''}"
					>
						<input
							hidden
							type="radio"
							name="day"
							value={day.format("YYYY-MM-DD")}
							disabled={!canBeSelected}
						/>
						{day.get("D")}
					</label>
				{/each}
			{/key}
		</div>
	</div>
</section>

<style>
	label:has(input:checked){
		color: white;
		background-color: #1e2939; 
	}
</style>
