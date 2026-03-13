<script lang="ts">
	interface Props {
		type: 'ingoing' | 'outgoing';
		username: string;
		message: string;
		avatar?: string;
	}

	let { 
		type, 
		username, 
		message, 
		avatar = "https://placehold.co/200x/ffa8e4/ffffff.svg?text=ʕ•́ᴥ•̀ʔ&font=Lato" 
	}: Props = $props();

	const isOutgoing = $derived(type === 'outgoing');
</script>

<div class="flex mb-4 cursor-pointer {isOutgoing ? 'justify-end' : ''}">
	{#if !isOutgoing}
		<div class="w-9 h-9 rounded-full flex items-center justify-center mr-2">
			<img src={avatar} alt="User Avatar" class="w-8 h-8 rounded-full" />
		</div>
	{/if}

	<div 
		class="flex flex-col max-w-96 rounded-lg p-3 gap-1 
		{isOutgoing ? 'bg-indigo-500 text-white' : 'bg-white text-gray-700'}"
	>
		<small class="text-xs">{username}</small>
		<p class={!isOutgoing ? 'text-gray-700' : ''}>{message}</p>
	</div>

	{#if isOutgoing}
		<div class="w-9 h-9 rounded-full flex items-center justify-center ml-2">
			<img 
				src="https://placehold.co/200x/b7a8ff/ffffff.svg?text=ʕ•́ᴥ•̀ʔ&font=Lato" 
				alt="My Avatar" 
				class="w-8 h-8 rounded-full" 
			/>
		</div>
	{/if}
</div>