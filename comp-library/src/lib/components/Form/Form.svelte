<script lang="ts">
	import FieldSet, { type Answer, type Question } from './FieldSet.svelte';
	import { cubicOut } from 'svelte/easing';
	import { fly } from 'svelte/transition';

	let { questions }: { questions: Question[] } = $props();
	let currentQuestionIndex = $state(0);
	let currentQuestion = $derived(questions[currentQuestionIndex]);
	let answers = $state<Answer[]>([]);
	let currentAnswer = $derived<Answer | null>(answers[currentQuestionIndex] ?? null);
	let movingForward = $state(1);

	function handleAnswer(answer: Answer): void {
		answers[currentQuestionIndex] = answer;
		nextQuestion();
	}

	function nextQuestion() {
		movingForward = 1;
		currentQuestionIndex = Math.min(currentQuestionIndex + 1, questions.length - 1);
	}

	function previousQuestion() {
		movingForward = -1;
		currentQuestionIndex = Math.max(currentQuestionIndex - 1, 0);
	}
</script>

<section
	class="flex aspect-7/6 w-full max-w-sm overflow-hidden rounded-xl border border-gray-500 p-2"
>
	<form class="flex flex-1 flex-col gap-3">
		<div class="grid grid-cols-1 grid-rows-1">
			{#key currentQuestionIndex}
				<div
					in:fly={{ x: 50 * movingForward, easing: cubicOut, duration: 600 }}
					out:fly={{ x: -50 * movingForward, easing: cubicOut, duration: 600 }}
					class="col-start-1 row-start-1"
				>
					<FieldSet question={currentQuestion} answer={currentAnswer} onAnswer={handleAnswer} />
				</div>
			{/key}
		</div>
		<!-- Action buttons -->
		<div class="flex w-full items-center">
			{#if currentQuestionIndex > 0}
				<button
					type="button"
					onclick={previousQuestion}
					class="scale-100 cursor-pointer rounded-xl bg-[#eae9e5] px-4 py-2 text-sm font-medium shadow-xs transition-all duration-100 active:scale-95 disabled:pointer-events-none disabled:opacity-30"
					>Volver</button
				>
			{/if}

			{#if currentQuestionIndex === questions.length - 1 && currentAnswer !== null}
				<button
					type="button"
					class="ml-auto scale-100 cursor-pointer rounded-xl bg-[#eae9e5] px-4 py-2 text-sm font-medium shadow-xs transition-all duration-100 active:scale-95 disabled:pointer-events-none disabled:opacity-30"
					>Finalizar</button
				>
			{:else if currentAnswer !== null}
				<button
					style="background-color: blue;"
					type="button"
					onclick={nextQuestion}
					class="ml-auto scale-100 cursor-pointer rounded-xl bg-[#eae9e5] px-4 py-2 text-sm font-medium shadow-xs transition-all duration-100 active:scale-95"
					>Siguiente</button
				>
			{/if}
			<button class="h-10 w-full bg-blue-500" style="background-color: blue;"> hola</button>
		</div>
	</form>
</section>
