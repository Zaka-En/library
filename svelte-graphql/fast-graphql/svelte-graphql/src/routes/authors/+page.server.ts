import type { PageServerLoad } from "./$types";
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ fetch }) => {
  const API_URL = env.PUBLIC_INTERNAL_API_URL || env.PUBLIC_API_URL || 'http://backend:8000/graphql';

  const OPTIONS = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `
        query {
          authors { id name biography country }
        }
      `
    })
  }

  const response = await fetch(API_URL, OPTIONS);
  const data = await response.json()

  return { authors: data.data?.authors ?? [] };
}