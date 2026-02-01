import { Client, cacheExchange, fetchExchange } from "@urql/svelte"
import { env } from '$env/dynamic/public';
import { browser } from '$app/environment';

const PUBLIC_URL = env.PUBLIC_API_URL || 'http://localhost:8000/graphql';
const INTERNAL_URL = env.PUBLIC_INTERNAL_API_URL || 'http://backend:8000/graphql';

const API_URL = browser ? PUBLIC_URL : INTERNAL_URL;

export const client = new Client({
  url: API_URL,
  exchanges: [cacheExchange, fetchExchange]
});

export const createClient = (fetch: typeof globalThis.fetch) => new Client({
  url: API_URL,
  exchanges: [cacheExchange, fetchExchange],
  fetch
});

// Alias for backward compatibility
export const mutationClient = client;
export const queryClient = client;

