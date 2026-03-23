<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { HTMLButtonAttributes } from 'svelte/elements';

	interface ButtonProps {
		size?: 'xs' | 'sm' | 'md';
		isLoading?: boolean;
		variant: 'action' | 'outline' | 'danger' | 'success' | 'warning';
		children?: Snippet;
		type?: 'button' | 'submit' | 'reset';
		restProps?: HTMLButtonAttributes;
		onclick?: () => void;
	}

	let { size = 'sm', isLoading = false, variant, children, ...restProps }: ButtonProps = $props();

	const sizeStyles = {
		xs: { button: 'text-xs py-1 px-2', loader: 16 },
		sm: { button: 'text-sm py-2 px-4', loader: 18 },
		md: { button: 'text-base py-3 px-6', loader: 20 }
	};

	const commonStyles =
		'cursor-pointer rounded-xl scale-100 active:scale-95 transition-all duration-100 font-medium disabled:opacity-30 disabled:pointer-events-none';
	const buttonStyles = {
		action: 'shadow-xs bg-secondary text-primary',
		outline: 'shadow-xs bg-transparent border border-primary-4',
		danger: 'shadow-xs bg-danger text-white',
		success: 'shadow-xs bg-success text-white',
		warning: 'shadow-xs bg-warning text-white'
	};
</script>

<button class="{commonStyles} {sizeStyles[size]?.button} {buttonStyles[variant]}" {...restProps}>
	<span class="relative flex flex-row items-center justify-center">
		{#if isLoading}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width={sizeStyles[size]?.loader || 20}
				height={sizeStyles[size]?.loader || 20}
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="absolute right-1/2 translate-x-1/2 animate-spin"
			>
				<path d="M21 12a9 9 0 1 1-6.219-8.56" />
			</svg>
		{/if}
		<span class={isLoading ? 'invisible' : ''}>
			{#if children}
				{@render children()}
			{/if}
		</span>
	</span>
</button>
