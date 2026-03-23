<script lang="ts" module>
	export interface Answer {
		id: string;
		score: number;
	}
	export interface Option {
		text: string;
		score: number;
	}

	export interface Question {
		id: string;
		question: string;
		options: Option[];
	}
</script>

<script lang="ts">
	interface Props {
		question: Question;
		answer: Answer | null;
		onAnswer: (answer: Answer) => void;
	}

	let { question, answer, onAnswer }: Props = $props();
</script>

<fieldset class="flex w-full flex-col gap-3">
	<legend class=" mb-3 flex min-h-12 items-center justify-center leading-6 font-semibold"
		>{question.question}</legend
	>
	{#each question.options as option (option.text)}
		<label class="cursor-pointer rounded-md border border-gray-400 px-3 py-2 hover:bg-[#eae9e570]">
			<input
				hidden
				type="radio"
				name={question.id}
				value={option.score}
				onchange={() => onAnswer({ id: question.id, score: option.score })}
				checked={answer?.score === option.score}
			/>
			{option.text}
		</label>
	{/each}
</fieldset>

<style>
	label:has(input:checked) {
		background-color: #eae9e5;
	}
</style>
