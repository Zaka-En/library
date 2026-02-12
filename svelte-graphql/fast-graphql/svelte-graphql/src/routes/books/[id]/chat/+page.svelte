<script lang="ts">
  import { onMount } from "svelte";
  import type { PageProps } from "./$types";
  import ChatMessage from "$lib/components/ChatMessage.svelte";
  import { SvelteMap } from "svelte/reactivity";

  interface Message{
    message: string
    username: string
    type: "ingoing" | "outgoing"
  }
  let { data } : PageProps = $props()

  // State & Derived
  const bookStore = $derived(data.bookStore);
  const bookTitle = $derived($bookStore.data?.book?.title) ;
  const bookId = $derived($bookStore.data?.book?.id)
  const bookChatSubStore = $derived(data.bookChatSubStore);
  const sendBookChatMessageStore = $derived(data.sendBookChatMessageStore);
  let lastMessage = $derived($bookChatSubStore.data?.bookChat)

  //Map to store 
  const messagesMap = $state(new SvelteMap<string, Message>());
  let inputMessage = $state("")

  $effect(() => {
    if (lastMessage) {
      const firstColonIndex = lastMessage.indexOf(': ');

      if(firstColonIndex !== -1){
        const username = lastMessage.slice(0,firstColonIndex)
        const message = lastMessage.slice(firstColonIndex + 2)
        
          const messageId = crypto.randomUUID()
          const newMessage: Message = {
            username,
            message,
            type: username === "YO" ? "outgoing" : "ingoing"
          }
          
          messagesMap.set(messageId, newMessage)
      }
    }
  })

  $effect(() => {
    if (messagesMap.size > 0 && bookTitle) {
      const dataToSave = JSON.stringify(Array.from(messagesMap.entries()).slice(-100));
      localStorage.setItem(`chat_${bookTitle}`, dataToSave);
    }
  })

  onMount(() => {

    if(bookId) bookChatSubStore.listen({bookId});
   

    if (bookTitle) {
      const saved = localStorage.getItem(`chat_${bookTitle}`);
      if (saved) {
        const parsed = JSON.parse(saved);
        // Hidratamos el SvelteMap
        messagesMap.clear();
        parsed.forEach(([id, msg]: [string, Message]) => messagesMap.set(id, msg));
      }
    }

    return () => {
      bookChatSubStore.unlisten();
    };
  });

  const sendMessage = async () => {
    if (!inputMessage || inputMessage.trim() ==="") {
      return;
    }

    const myUsername = "YO"; 

    try {
      if (bookId) {
        await sendBookChatMessageStore.mutate({ 
          bookId,
          userName: myUsername, 
          message: inputMessage 
         });
      }
    } catch (error) {
      console.error("error sending the message", error)
    }
    inputMessage = ""
  }

  // Debug y inspect
  $inspect(lastMessage)

</script>

<article 
 class="fixed flex inset-0 flex-col bg-gray-100 overflow-hidden">
  <header class="shrink-0 bg-white p-4 text-gray-700 shadow-sm z-20">
    <h1 class="text-2xl font-semibold">Chat de "{bookTitle}"</h1>
  </header>

  <section class="flex-1 overflow-y-auto p-4 space-y-2">
    {#each messagesMap.entries() as [id, msg] (id)}
      <ChatMessage
        message={msg.message}
        type={msg.type}
        username={msg.username}
      />
    {/each}
  </section>

  <footer class="shrink-0 sticky bottom-0 bg-white border-t border-gray-300 p-4 z-20">
    <div class="flex items-center max-w-4xl mx-auto">
      <input 
        bind:value={inputMessage}
        onkeydown={(e: KeyboardEvent) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
          }
        }}
        type="text" 
        placeholder="Escribe tu mensaje..." 
        class="flex-1 p-2 rounded-md border border-gray-400 focus:outline-none focus:border-indigo-500"
      >
      <button onclick={sendMessage}
        class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-md ml-2 transition-colors cursor-pointer">
        Enviar
      </button>
    </div>
  </footer>
</article>