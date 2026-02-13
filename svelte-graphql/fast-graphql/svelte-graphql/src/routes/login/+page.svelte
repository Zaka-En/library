<script lang="ts">
  import { enhance } from "$app/forms";

  let { form }  = $props()

</script>

<section class="bg-gray-50 dark:bg-gray-900 w-full max-w-md p-4 sm:p-6 rounded-lg shadow-xl flex flex-col items-center mt-5 mx-auto">
    
    <a href="#d" class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
        <img class="w-8 h-8 mr-2" src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/logo.svg" alt="logo">
        Biblio    
    </a>

    <div class="w-full bg-white rounded-lg shadow dark:border dark:bg-gray-800 dark:border-gray-700">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
            <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                Introduzca sus credenciales
            </h1>
            
            <form use:enhance method="POST" class="space-y-4 md:space-y-6">
                <div>
                    <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">email</label>
                    <input type="email" name="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="name@company.com" required>
                </div>

                <div>
                    <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">contraseña</label>
                    <input type="password" name="password" id="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white" required>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-start">
                        <div class="flex items-center h-5">
                            <input id="remember" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600">
                        </div>
                        <div class="ml-3 text-sm">
                            <label for="remember" class="text-gray-500 dark:text-gray-300">Recuérdame</label>
                        </div>
                    </div>
                    <a href="#restore" class="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500">¿olvidé mi contraseña?</a>
                </div>

                <button type="submit" class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                    Iniciar sesión
                </button>

                <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                    ¿Todavía no tienes cuenta? <a href="#bla" class="font-medium text-blue-600 hover:underline dark:text-blue-500">Regístrate ahora</a>
                </p>

                {#if form?.error}
                    <p class="p-2 text-sm text-center text-red-600 bg-red-100 rounded border border-red-200">{form.error}</p>
                {/if}
            </form>
        </div>
    </div>
</section>