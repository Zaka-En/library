import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {
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

  const URL_SERVIDOR = 'http://localhost:8000/graphql'

  const response = await fetch(URL_SERVIDOR, OPTIONS); 
  const data = await response.json()
  

  return { authors: data.data.authors };
  
}